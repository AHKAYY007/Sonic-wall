from fastapi import FastAPI, Depends, WebSocket
from sqlalchemy.orm import Session
from . import model, schemas, database, crud, websocket
from fastapi.middleware.cors import CORSMiddleware

model.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)

@app.get("/api/traffic")
def get_traffic(db: Session = Depends(get_db)):
    return crud.get_traffic(db)

@app.post("/api/traffic")
async def add_call(call: schemas.ContractCallCreate, db: Session = Depends(get_db)):
    new_call = crud.create_call(db, call)
    await websocket.manager.broadcast({
        "event": "new_call",
        "data": schemas.ContractCallOut.from_orm(new_call).dict()
    })
    return new_call

@app.get("/api/blocked")
def get_blocked(db: Session = Depends(get_db)):
    return crud.get_blocked(db)

@app.post("/api/blocked")
def block_address(addr: schemas.BlockedAddressBase, db: Session = Depends(get_db)):
    return crud.block_address(db, addr.address)

@app.delete("/api/blocked/{addr}")
def unblock(addr: str, db: Session = Depends(get_db)):
    return crud.unblock_address(db, addr)

@app.websocket("/ws/traffic")
async def traffic_ws(ws: WebSocket):
    await websocket.manager.connect(ws)
    try:
        while True:
            await ws.receive_text()  # keep alive
    except:
        websocket.manager.disconnect(ws)
