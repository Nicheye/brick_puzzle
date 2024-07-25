from prompts.celery import app


@app.task
def generate_image(prompt, style, color):
    pass