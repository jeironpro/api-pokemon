from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, select
from database.connection import engine, obtener_db
from models.Pokemon import Pokemon, PokemonRequest, TipoPokemon, TipoPokemonEnlace, EstadisticasPokemon, PokemonResponse
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import joinedload

app = FastAPI(
    title="API Pokemón",
    version="1.0"
)

# Crear las tablas al iniciar el servidor
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/agregar_pokemon", response_model=dict, tags=["Agregar pokemon"])
def agregar_pokemon(pokemon: PokemonRequest, db: Session = Depends(obtener_db)):
    nuevo_pokemon = Pokemon(nombre=pokemon.nombre, descripcion=pokemon.descripcion)
    db.add(nuevo_pokemon)
    db.flush()

    for tipo_pokemon in pokemon.tipos:
        tipo = db.exec(select(TipoPokemon).where(TipoPokemon.nombre == tipo_pokemon.nombre)).first()

        if not tipo:
            tipo = TipoPokemon(nombre=tipo_pokemon.nombre)
            db.add(tipo)
            db.flush()

        enlace = TipoPokemonEnlace(pokemon_id=nuevo_pokemon.id, tipo_id=tipo.id)
        db.add(enlace)

    estadisticas = EstadisticasPokemon(
        punto_salud=pokemon.estadisticas.punto_salud,
        ataque=pokemon.estadisticas.ataque,
        defensa=pokemon.estadisticas.defensa,
        ataque_especial=pokemon.estadisticas.ataque_especial,
        defensa_especial=pokemon.estadisticas.defensa_especial,
        velocidad=pokemon.estadisticas.velocidad,
        pokemon_id=nuevo_pokemon.id
    )
    
    db.add(estadisticas)
    db.commit()
    db.refresh(nuevo_pokemon)

    return {"msg": "Pokemon creado correctamente"}

@app.get("/pokemones", response_model=List[PokemonResponse], tags=["Obtener pokemones"])
def obtener_pokemones(db: Session = Depends(obtener_db)):
    consulta = (
        select(Pokemon)
        .options(
            joinedload(Pokemon.tipos),
            joinedload(Pokemon.estadisticas)
        )
    )

    pokemones = db.exec(consulta).unique().all()
    return pokemones

@app.get("/pokemon_id", response_model=PokemonResponse, tags=["Obtener pokemon por id"])
def obtener_pokemon_id(id: int, db: Session = Depends(obtener_db)):
    consulta = select(Pokemon).where(Pokemon.id == id)
    pokemon = db.exec(consulta).first()
    return pokemon

@app.get("/pokemones_tipo", response_model=List[PokemonResponse], tags=["Obtener pokemones por tipo"])
def obtener_pokemones_tipo(tipo: str, db: Session = Depends(obtener_db)):
    consulta = (
        select(Pokemon)
        .join(Pokemon.tipos)
        .where(func.lower(TipoPokemon.nombre) == tipo.lower())
        .options(
            joinedload(Pokemon.tipos),
            joinedload(Pokemon.estadisticas)
        )
    )

    pokemones = db.exec(consulta).unique().all()
    return pokemones