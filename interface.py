import gradio as gr

from pipeline import PipelineRAG

pipe = PipelineRAG()

with gr.Blocks() as demo:
    gr.Markdown("# Sub-Task Formulator Chatbot")
    gr.Markdown("Enter a complex question, and I will break it down into policy and database sub-questions.")

    user_input = gr.Textbox(label="Your complex question", placeholder="e.g., Can an employee be denied access to remote work tools after policy change?")
    subtasks = gr.Textbox(label="Decomposed Sub-Questions", lines=1)

    subtasks_w_answers = gr.Textbox(label="Sub-Tasks with Answers", lines=2)
    
    compiled_ans = gr.Textbox(label="Compiled Answer", lines=1)

    btn = gr.Button("Decompose Question")
    btn.click(fn=pipe.run, inputs=user_input, outputs=[subtasks, subtasks_w_answers, compiled_ans])

demo.launch()