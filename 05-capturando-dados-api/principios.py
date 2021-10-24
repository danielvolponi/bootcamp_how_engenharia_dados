import datetime
import math

class Pessoa:
    def __init__(self, 
                nome: str, 
                sobrenome: str, 
                data_de_nascimento: datetime.date
            ) -> None:
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_de_nascimento = data_de_nascimento

    # Atributo da Pessoa derivado da data de nascimento
    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)

    def __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos."


class Curriculo:
    def __init__(self, pessoa: Pessoa, experiencias: List[str]):
        self.pessoa = pessoa
        self.experiencias = experiencias

andre = Pessoa(nome='Andre', sobrenome='Sionek', data_de_nascimento=datetime.date(1991,1,9))
print(andre)

curriculo_andre = Curriculo(pessoa=andre, experiencias=['HSBC', 'Polyteck', 'Grupo Boticário', 'Olist', 'EmCasa' , 'Gousto'])