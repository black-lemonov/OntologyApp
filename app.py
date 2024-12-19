import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext, messagebox

from rdflib import Graph


class App:
    GRAPH_IRI: str = "/home/egorp/Учеба/Модели ИС/Охрана_природы_исправленная.rdf"
    
    def __init__(self):
        self._set_graph()
        self._set_root()
        self._set_output_field()
        self._set_input_field()
        self._set_buttons()

    def _set_graph(self) -> None:
        '''Создание и загрузка графа RDF'''
        self.__graph = Graph()
        self.__graph.parse(self.GRAPH_IRI)  # Пример загрузки данных из URL

    def _set_root(self) -> None:
        '''Создание главного окна'''
        self.__root = tk.Tk()
        self.__root.title("Охрана Природы")
    
    def _set_output_field(self) -> None:
        '''Создание поля для вывода результатов запроса'''
        ttk.Label(
            self.__root,
            text="Результат",
        ).pack(
            side="top",
            expand=True,
            fill='x',
            pady=10,
            padx=10
        )
        self.__result_output = scrolledtext.ScrolledText(self.__root, width=60, height=10)
        self.__result_output.pack(
            side='top',
            expand=True,
            fill="both",
            pady=10,
            padx=10
        )
        
    def _set_input_field(self) -> None:
        '''Создание поля для ввода пользовательского SPARQL запроса'''
        ttk.Label(
            self.__root,
            text="Запрос",
        ).pack(
            side="top",
            fill="x",
            pady=10
        )
        self.__query_input = scrolledtext.ScrolledText(self.__root, width=60, height=10)
        self.__query_input.pack(
            side='top',
            fill="both",
            expand=True,
            pady=10,
            padx=10
        )
        
    def _set_buttons(self) -> None:
        '''Создание кнопок для выполнения запросов'''
        predefined_queries: dict[str, str] = {
            "Активисты" : """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX ont: <http://www.semanticweb.org/egorp/ontologies/2024/11/untitled-ontology-20#>
            SELECT ?Активист
	            WHERE {?Активист rdf:type ont:Activist}
            """,
            "Материалы" : """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX ont: <http://www.semanticweb.org/egorp/ontologies/2024/11/untitled-ontology-20#>
            SELECT ?материал ?название
	            WHERE { ?материал ont:Название_материала ?название }
            """,
            "Законы" : """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX ont: <http://www.semanticweb.org/egorp/ontologies/2024/11/untitled-ontology-20#>
            SELECT ?закон ?проблема
	            WHERE {?закон ont:Закон_о_Проблеме ?проблема}
            """
        }
        
        for query_name, query in predefined_queries.items():
            button = ttk.Button(self.__root, text=query_name, command=lambda q=query: self._run_predefined_query(q))
            button.pack(
                side='right'
            )
            
        self.__execute_button = ttk.Button(
            self.__root, 
            text="Выполнить запрос",
            command=self._run_custom_query
        )
        self.__execute_button.pack(
            side='right'
        )

    def _execute_query(self, query) -> str:
        try:
            results = self.__graph.query(query)
            result_str = ""
            for row in results:
                result_str += str(row) + "\n"
            return result_str.strip()
        except Exception as e:
            return str(e)

    def _run_custom_query(self):
        query = self.__query_input.get("1.0", tk.END).strip()
        if query:
            result = self._execute_query(query)
            self.__result_output.delete("1.0", tk.END)
            self.__result_output.insert(tk.END, result)
        else:
            messagebox.showwarning("Warning", "Введите SPARQL запрос.")

    def _run_predefined_query(self, query):
        result = self._execute_query(query)
        self.__result_output.delete("1.0", tk.END)
        self.__result_output.insert(tk.END, result)

    def run(self) -> None:
        self.__root.mainloop()


if __name__ == "__main__":
    App().run()
