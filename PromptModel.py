from openai import OpenAI

def prompt_model(prompt):
    client = OpenAI(
        organization='org-miLxPVrUMo3EKEXwFxGkDoiS',
        project='proj_oS3d7Rnjgr141tDhCN7hZohr',
    )
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "user", 'content': prompt}
        ]
    )
    return completion.choices[0].message.content