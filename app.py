import gradio as gr
from retrieve import retrieve
from generator import generate_response

def handle_query(question):
    if not question.strip():
        return ""
    
    relevant_info = retrieve(question)
    response, sources = generate_response(question, relevant_info)
    return response, sources

with gr.Blocks() as demo:
    inp = gr.Textbox(label="Your question")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()