import gradio as gr

from pipeline import PipelineRAG

pipe = PipelineRAG()

with gr.Blocks() as demo:
    gr.Markdown("# HR Replacer")
    gr.Markdown("Ask me a question regarding your company HRMS stuff.")

    user_input = gr.Textbox(label="Your question", placeholder="Hi! I am an HRMS Chatbot!!")
    subtasks = gr.Textbox(label="Decomposed Sub-Questions", lines=1)

    subtasks_w_answers = gr.Textbox(label="Sub-Tasks with Answers", lines=2)
    
    compiled_ans = gr.Textbox(label="Compiled Answer", lines=1)

    btn = gr.Button("Decompose Question")
    btn.click(fn=pipe.run, inputs=user_input, outputs=[subtasks, subtasks_w_answers, compiled_ans])

demo.launch()