from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.states.blogstate import BlogState
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self,llm):
        self.llm=llm

    def build_topic_graph(self):
        """
        Build a graph to generate blogs based on topic with language support
        """
        graph = StateGraph(BlogState)
        self.blog_node_obj=BlogNode(self.llm)
        ## Nodes
        graph.add_node("title_creation", self.blog_node_obj.title_creation)
        graph.add_node("content_generation",self.blog_node_obj.content_generation)
        graph.add_node("translation", self.blog_node_obj.translation)
        graph.add_node("route",self.blog_node_obj.route)

        ## Edges
        graph.add_edge(START,"title_creation")
        graph.add_edge("title_creation","content_generation")
        graph.add_edge("content_generation", "route")

        ## conditional edge for language translation
        graph.add_conditional_edges(
            "route",
            self.blog_node_obj.route_decision,
            {
                "translate":"translation",
                "end":END
            }
        )
        graph.add_edge("translation",END)

        return graph
    
    def build_youtube_graph(self):
        """
        Build a graph for blog generation from YouTube transcript
        """
        graph = StateGraph(BlogState)
        self.blog_node_obj=BlogNode(self.llm)
        ## Nodes
        graph.add_node("extract_transcript", self.blog_node_obj.extract_youtube_transcript)
        graph.add_node("generate_blog_from_transcript", self.blog_node_obj.generate_blog_from_transcript)
        graph.add_node("translation", self.blog_node_obj.translation)
        graph.add_node("route", self.blog_node_obj.route)

        ## Edges
        graph.add_edge(START, "extract_transcript")
        graph.add_edge("extract_transcript", "generate_blog_from_transcript")
        graph.add_edge("generate_blog_from_transcript", "route")
        
        ## conditional edge
        graph.add_conditional_edges(
            "route",
            self.blog_node_obj.route_decision,
            {
                "translate":"translation",
                "end":END
            }
        )
        graph.add_edge("translation",END)
        return graph

    
    def setup_graph(self,usecase):
        if usecase=="topic":
            return self.build_topic_graph().compile()
        elif usecase=="youtube":
            return self.build_youtube_graph().compile()
        else:
            raise ValueError(f"Unknown usecase: {usecase}")
    

## Below code is for the langsmith langgraph studio
llm=GroqLLM().get_llm()

## get the graph
graph_builder=GraphBuilder(llm)
graph=graph_builder.build_topic_graph().compile()

