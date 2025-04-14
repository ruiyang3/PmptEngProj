import gradio as gr

with gr.Blocks() as demo:
    gr.Markdown("# Sub-Task Formulator Chatbot")
    gr.Markdown("Enter a complex question, and I will break it down into policy and database sub-questions.")

    user_input = gr.Textbox(label="Your complex question", placeholder="e.g., Can an employee be denied access to remote work tools after policy change?")
    output = gr.Textbox(label="Decomposed Sub-Questions", lines=2)

    btn = gr.Button("Decompose Question")

    btn.click(fn=prompt_model, inputs=user_input, outputs=output)

demo.launch()