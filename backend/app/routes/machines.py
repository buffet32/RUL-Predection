from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Machine
from app.schemas import MachineCreate, MachineUpdate, MachineResponse

router = APIRouter(prefix="/machines", tags=["machines"])


@router.post("/", response_model=MachineResponse, status_code=201)
async def create_machine(machine: MachineCreate, db: Session = Depends(get_db)):
    """
    Create a new machine
    """
    # Check if machine name already exists
    existing = db.query(Machine).filter(Machine.name == machine.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Machine name already exists")
    
    db_machine = Machine(**machine.model_dump())
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    
    return db_machine


@router.get("/", response_model=List[MachineResponse])
async def get_machines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all machines with pagination
    """
    machines = db.query(Machine).offset(skip).limit(limit).all()
    return machines


@router.get("/{machine_id}", response_model=MachineResponse)
async def get_machine(machine_id: int, db: Session = Depends(get_db)):
    """
    Get a specific machine by ID
    """
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine


@router.put("/{machine_id}", response_model=MachineResponse)
async def update_machine(machine_id: int, machine_update: MachineUpdate, db: Session = Depends(get_db)):
    """
    Update a machine
    """
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    for field, value in machine_update.model_dump(exclude_unset=True).items():
        setattr(machine, field, value)
    
    db.commit()
    db.refresh(machine)
    
    return machine


@router.delete("/{machine_id}", status_code=204)
async def delete_machine(machine_id: int, db: Session = Depends(get_db)):
    """
    Delete a machine
    """
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    db.delete(machine)
    db.commit()
    
    return None
