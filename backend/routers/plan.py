from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from vector.vector_store import add_memory, search_memory
from graph import build_graph
from db.database import get_db
from db import models
from fastapi.responses import StreamingResponse
import asyncio

router = APIRouter(
    prefix="/plan",
    tags=["plan"],
)

# Initialize graph once
graph = build_graph()


class PlanRequest(BaseModel):
    idea: str

@router.post("/")
def generate_plan(
    request: PlanRequest,
    db: Session = Depends(get_db)
):

    if not request.idea.strip() or len(request.idea.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Idea must be at least 10 characters long"
        )

    try:
        similar_docs = search_memory(request.idea)
        memory_context = "\n".join([doc.page_content for doc in similar_docs])

        result = graph.invoke({
            "idea": request.idea,
            "memory_context": memory_context
        })

        add_memory(request.idea)

        conversation = models.Conversation(
            user_input=request.idea,
            clarified_idea=result.get("clarified_idea"),
            execution_plan=result.get("plan"),
            risks=result.get("risks"),
            tools=result.get("tools"),
            market_analysis=result.get("market_analysis"),
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return {
            "clarified_idea": result.get("clarified_idea"),
            "execution_plan": result.get("plan"),
            "risks": result.get("risks"),
            "tools_and_resources": result.get("tools"),
            "market_analysis": result.get("market_analysis"),
        }

    except Exception as e:   
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/history")
def get_history(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    conversations = (
        db.query(models.Conversation)
        .order_by(models.Conversation.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return conversations

@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    conversation = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    db.delete(conversation)
    db.commit()

    return {"message": "Deleted successfully"}

@router.get("/search")
def search_conversations(
    query: str,
    db: Session = Depends(get_db)
):
    results = db.query(models.Conversation).filter(
        models.Conversation.user_input.contains(query)
    ).all()

    return results

@router.post("/stream")
async def stream_plan(
    request: PlanRequest,
    db: Session = Depends(get_db)
):

    async def generate():
  
        await asyncio.sleep(0.8)

        result = graph.invoke({
            "idea": request.idea,
            "memory_context": ""
        })

        # Save to DB
        conversation = models.Conversation(
            user_input=request.idea,
            clarified_idea=result.get("clarified_idea"),
            execution_plan=result.get("plan"),
            risks=result.get("risks"),
            tools=result.get("tools"),
            market_analysis=result.get("market_analysis"),
        )
        db.add(conversation)
        db.commit()

        # Stream full response at once
        full_response = f"""
        Clarified Vision:\n
        {result.get("clarified_idea")}

        Execution Roadmap:\n
        {result.get("plan")}

        Risk Assessment:\n
        {result.get("risks")}

        Technical Strategy:\n
        {result.get("tools")}

        Market Positioning:\n
        {result.get("market_analysis")}
        """

        yield full_response


    return StreamingResponse(generate(), media_type="text/plain")
