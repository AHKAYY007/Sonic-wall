from fastapi import FastAPI, Depends, WebSocket, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import model, schemas, database, crud, websocket

# ---------- Database Setup ----------
model.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Middleware ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Root ----------
@app.get("/")
async def root():
    return {"message": "Hello World"}

# ---------- Stats ----------
@app.get("/api/stats", response_model=dict)
def get_stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)

@app.get("/api/stats/latency", response_model=float)
def average_latency(db: Session = Depends(get_db)):
    return crud.get_average_latency(db)

# ---------- Traffic ----------
@app.get("/api/traffic", response_model=List[schemas.ContractCallOut])
def get_traffic(db: Session = Depends(get_db)):
    return crud.get_traffic(db)

@app.post("/api/traffic", response_model=schemas.ContractCallOut)
async def add_call(call: schemas.ContractCallCreate, db: Session = Depends(get_db)):
    new_call = crud.create_call(db, call)
    await websocket.manager.broadcast({
        "event": "new_call",
        "data": schemas.ContractCallOut.model_validate(new_call).model_dump()
    })
    return new_call

# ---------- Blocked ----------
@app.get("/api/blocked", response_model=List[schemas.BlockedAddressOut])
def get_blocked(db: Session = Depends(get_db)):
    return crud.get_blocked(db)

@app.get("/api/blocked/{addr}", response_model=schemas.BlockedAddressOut)
def get_blocked_address(addr: str, db: Session = Depends(get_db)):
    return crud.get_blocked_address(db, addr)

@app.get("/api/blocked/{addr}/exists", response_model=bool)
def is_blocked(addr: str, db: Session = Depends(get_db)):
    return crud.is_blocked(db, addr)

@app.post("/api/blocked", response_model=schemas.BlockedAddressOut)
def block_address(addr: schemas.BlockedAddressBase, db: Session = Depends(get_db)):
    return crud.block_address(db, addr.address)

@app.delete("/api/blocked/{addr}", response_model=dict)
def unblock(addr: str, db: Session = Depends(get_db)):
    return {"success": crud.unblock_address(db, addr)}

# ---------- Wallet ----------
@app.get("/api/wallet/{address}/history", response_model=List[schemas.ContractCallOut])
def wallet_history(address: str, db: Session = Depends(get_db)):
    return crud.get_wallet_history(db, address)

@app.get("/wallet/{address}/sync", response_model=List[schemas.ContractCallOut])
def sync_wallet(address: str, db: Session = Depends(get_db)):
    crud.sync_wallet_transactions(db, address)
    return crud.get_wallet_transactions(db, address)



@app.get("/wallet/{address}/transactions")
def get_wallet_transactions(address: str, db: Session = Depends(get_db)):
    crud.sync_wallet_transactions(db, address)
    return crud.get_wallet_transactions(db, address)

# ---------- WebSocket ----------
@app.websocket("/ws/traffic")
async def traffic_ws(ws: WebSocket):
    await websocket.manager.connect(ws)
    try:
        while True:
            await ws.receive_text()
    except:
        websocket.manager.disconnect(ws)

