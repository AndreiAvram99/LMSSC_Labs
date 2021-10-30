from aifc import Error
from typing import List
from enum import Enum


class GenerationError(Error):
    def __init__(self, message):
        self.message = message


class Orientation(Enum):
    Across = 0
    Down = 1


class CrossWord:
    def __init__(self, cross_word_text: str) -> None:
        self.cross_word_text = cross_word_text

    def __str__(self) -> str:
        return f"<Row>{self.cross_word_text.upper()}</Row>\n"


class Clue:
    def __init__(self,
                 row: int,
                 col: int,
                 num: int,
                 orientation: Orientation,
                 ans: str,
                 clue_text: str) -> None:

        self.row = row
        self.col = col
        self.num = num
        self.ans = ans
        self.clue_text = clue_text
        self.orientation = orientation

    def __str__(self) -> str:
        return f"<Clue Row=\"{self.row}\" " \
               f"Col=\"{self.col}\" " \
               f"Num=\"{self.num}\" " \
               f"Dir=\"{self.orientation.__str__()}\" " \
               f"Ans=\"{self.ans}\">" \
               f"![CDATA[{self.clue_text}]]</Clue>\n"


class CluesGenerator:
    def __init__(self, raw_clues: List[str]) -> None:
        self.raw_clues = raw_clues
        self.clues_list = []

    def generate_clues(self) -> None:
        for raw_clue in self.raw_clues:
            clue = Clue(row=0,
                        col=0,
                        num=0,
                        orientation=Orientation.Across,
                        ans="__________",
                        clue_text=raw_clue)
            self.clues_list.append(clue)

    def get_clues(self) -> List[CrossWord]:
        if len(self.clues_list) != 0:
            return self.clues_list
        else:
            raise GenerationError("You should generate clues first")


class CrossWordsGenerator:
    def __init__(self, raw_cross_words: List[str]) -> None:
        self.raw_cross_words = raw_cross_words
        self.cross_words_list = []

    def generate_cross_words(self) -> None:
        for raw_cross_word in self.raw_cross_words:
            cross_word = CrossWord(cross_word_text=raw_cross_word)
            self.cross_words_list.append(cross_word)

    def get_cross_words(self) -> List[CrossWord]:
        if len(self.cross_words_list) != 0:
            return self.cross_words_list
        else:
            raise GenerationError("You should generate cross words first")


class CrossWordsPuzzleGenerator:
    def __init__(self,
                 dimension: (int, int),
                 cross_words_generator: CrossWordsGenerator,
                 clues_generator: CluesGenerator
                 ) -> None:
        self.dimension = dimension
        self.cross_words_generator = cross_words_generator
        self.clues_generator = clues_generator
        self.cross_words_generator.generate_cross_words()
        self.clues_generator.generate_clues()

        try:
            self.cross_words_list = self.cross_words_generator.get_cross_words()
        except GenerationError:
            print("cross words list is empty")
            self.cross_words_list = []

        try:
            self.clues_list = self.clues_generator.get_clues()
        except GenerationError:
            print("clues list is empty")
            self.clues_list = []

    def create_cross_words_file(self) -> None:
        self.write_header_in_file()
        self.write_grid()
        self.write_clues()
        self.write_footer()

    def write_header_in_file(self) -> None:
        file = open("cross_words_file", "w")
        file.write("<?xml version='1.0' encoding='utf-8'?>\n")
        file.write("<Puzzles Version=\"1.0\">\n")
        file.write("<Puzzle>\n")
        file.write("<Size>\n")
        file.write(f"<Rows>{self.dimension[0]}</Rows>\n")
        file.write(f"<Cols>{self.dimension[1]}</Cols>\n")
        file.write("</Size>\n")
        file.close()

    def write_grid(self) -> None:
        file = open("cross_words_file", "a")
        file.write("<Grid>\n")
        for word in self.cross_words_list:
            file.write(word.__str__())
        file.write("</Grid>\n")

    def write_clues(self) -> None:
        file = open("cross_words_file", "a")
        file.write("<Clues>\n")
        for clue in self.clues_list:
            file.write(clue.__str__())
        file.write("</Clues>\n")

    @staticmethod
    def write_footer() -> None:
        file = open("cross_words_file", "a")
        file.write("</Puzzle>\n")
        file.write("</Puzzles>\n")


if __name__ == '__main__':
    words = ["apple", "pear", "plum", "peach"]
    clues = ["juicy red fruit growth in a tree",
             "yellow fruit",
             "round shaped violet fruit",
             "last name of a famous actor in Romania"]

    local_cross_word_generator = CrossWordsGenerator(raw_cross_words=words)
    local_clues_generator = CluesGenerator(raw_clues=clues)
    cross_words_puzzle_generator = CrossWordsPuzzleGenerator((4, 5), local_cross_word_generator, local_clues_generator)
    cross_words_puzzle_generator.create_cross_words_file()
