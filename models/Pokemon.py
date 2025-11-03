from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# Tabla intermedia con relación (N:N) entre Pokémon y Tipo
class TipoPokemonEnlace(SQLModel, table=True):
    pokemon_id: int = Field(foreign_key="pokemon.id", primary_key=True)
    tipo_id: int = Field(foreign_key="tipopokemon.id", primary_key=True)

class TipoPokemon(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)

    pokemons: List["Pokemon"] = Relationship(
        back_populates="tipos", 
        link_model=TipoPokemonEnlace
    )

class Pokemon(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)
    descripcion: str

    tipos: List["TipoPokemon"] = Relationship(
        back_populates="pokemons",
        link_model=TipoPokemonEnlace
    )
    estadisticas: Optional["EstadisticasPokemon"] = Relationship(
        back_populates="pokemon"
    )

class EstadisticasPokemon(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    punto_salud: int
    ataque: int
    defensa: int
    ataque_especial: int
    defensa_especial: int
    velocidad: int 
    pokemon_id: int = Field(foreign_key="pokemon.id", unique=True)

    pokemon: Optional[Pokemon] = Relationship(
        back_populates="estadisticas"
    )


class EstadisticasPokemonRequest(SQLModel):
    punto_salud: int
    ataque: int
    defensa: int
    ataque_especial: int
    defensa_especial: int
    velocidad: int 

class TipoPokemonRequest(SQLModel):
    nombre: str

class PokemonRequest(SQLModel):
    nombre: str
    descripcion: str
    tipos: List[TipoPokemonRequest]
    estadisticas: EstadisticasPokemonRequest

class PokemonResponse(SQLModel):
    id: int
    nombre: str
    descripcion: str
    tipos: List[TipoPokemonRequest] = []
    estadisticas: Optional[EstadisticasPokemonRequest] = None