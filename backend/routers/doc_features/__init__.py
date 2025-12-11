from fastapi import APIRouter, Body

import config

from openai import AsyncOpenAI

from . import schemes


router = APIRouter()


client = AsyncOpenAI(
    api_key=config.OPENAI_API_KEY
)




@router.post("/complicated-summary")
async def complicated_summary(content: str = Body(embed=True)) -> schemes.Response:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an expert document summarizer. Your task is to analyze a given document or contract and generate a detailed summary that preserves the original structure—such as headings, sections, and bullet points—and is written in the same language as the original document. Include all essential details (e.g., parties, terms, dates, obligations, etc.) in your summary. Your final output should consist solely of this summary, without any additional commentary. This summary will be used to answer user questions about the document.”"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"content: {content}"
                    }
                ]
            }
        ],
        response_format={
            "type": "text"
        },
        temperature=0.5,
        max_completion_tokens=2100
    )

    return {"res": response.choices[0].message.content}


@router.post("/key-points")
async def key_points(content: str = Body(embed=True)) -> schemes.Response:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an expert document analyzer. Your task is to read the provided document or contract and extract its key points while preserving the original structure (using headings, sections, and bullet points). Ensure your output is written in the same language as the original document. Use HTML markup (<b>, <i>, <span style='color:any color'>, <h1>, <h2>, <h3>) to format your summary. Provide only the final result in your answer. Make everything you write short."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"content: {content}"
                    }
                ]
            }
        ],
        response_format={
            "type": "text"
        },
        temperature=0.5,
        max_completion_tokens=2100
    )

    return {"res": response.choices[0].message.content}


@router.post("/summary")
async def summary(party: str, content: str = Body(embed=True)) -> schemes.Response:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an expert document analyzer. Your task is to read the provided document or contract and generate a summary using easy words, ensuring that the summary is understandable by someone who has never seen the original document. Carefully check the document for clarity and include all key points. Ensure your output is written in the same language as the original document. Use HTML markup (<b>, <i>, <span style='color:any color'>, <h1>, <h2>, <h3>) to format your summary. Provide only the final result in your answer. This summary should be useful for the party that will be bound by the document."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"content: {content};\nparty: {party}"
                    }
                ]
            }
        ],
        response_format={
            "type": "text"
        },
        temperature=0.5,
        max_completion_tokens=2100
    )

    return {"res": response.choices[0].message.content}




@router.post("/risks")
async def risks(party: str, content: str = Body(embed=True)) -> schemes.Response:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an expert contract analyzer. Your task is to analyze any provided document or contract, determine its type, and evaluate it for common risks affecting the party that will be bound by it. In addition, identify any other potential risks or missing details that could cause future problems. If the document was created by that party, also point out any errors, omissions, or gaps in the document. Your final output must be written in the same language as the original document and use HTML markup (<b>, <i>, <span style='color:any color'>, <h1>, <h2>, <h3>) for formatting. Provide only the final result in your answer."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"content: {content};\nparty: {party}"
                    }
                ]
            }
        ],
        response_format={
            "type": "text"
        },
        temperature=0.5,
        max_completion_tokens=2100
    )

    return {"res": response.choices[0].message.content}




@router.post("/additional-info")
async def additional_info(party: str, content: str = Body(embed=True)) -> schemes.Response:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an expert document analyzer. Your task is to read the provided document or contract and generate additional useful information for the party that will be bound by it. Using your expertise, identify and include any extra details, insights, or recommendations that were not coveany color in the previously mentioned summary of key points and risks. Your output must be written in the same language as the original document, and use HTML markup (<b>, <i>, <span style='color:any color'>, <h1>, <h2>, <h3>) for formatting. Provide only the final result in your answer."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"content: {content};\nparty: {party}"
                    }
                ]
            }
        ],
        response_format={
            "type": "text"
        },
        temperature=0.5,
        max_completion_tokens=2100
    )

    return {"res": response.choices[0].message.content}




@router.post("/explain-part")
async def explain_part(content: str = Body(embed=True), content_part: str = Body(embed=True)) -> schemes.Response:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an expert document analyzer. Your task is to read the provided document or contract and explain the specified part. In your explanation, describe what this part means and identify any risks, errors, or gaps it may have. If you do not understand the user’s request or cannot determine the answer, clearly state that you do not know. Ensure your output is written in the same language as the original document, and use HTML markup (<b>, <i>, <span style='color:any color'>, <h1>, <h2>, <h3>) for formatting. Provide only the final result in your answer"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"content:{content};\ncontent_part:{content_part}"
                    }
                ]
            }
        ],
        response_format={
            "type": "text"
        },
        temperature=0.5,
        max_completion_tokens=2100
    )

    return {"res": response.choices[0].message.content}




@router.post("/ask")
async def ask(question: str, content: str = Body(embed=True)) -> schemes.Response:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an expert Q&A assistant with comprehensive document analysis skills. Your task is to answer all user questions. When needed, refer to the provided document to incorporate relevant details—such as names, addresses, and other key information—into your response. Your output must be written in the same language as the original document and formatted using HTML markup (<b>, <i>, <span style='color:any color'>, <h1>, <h2>, <h3>) for clarity and emphasis. If you do not understand the user’s request or cannot determine the answer, clearly state that you do not know. Provide only the final answer in your response."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"question:{question}"
                    },
                    {
                        "type": "text",
                        "text": f"doc_summary:{content}"
                    }
                ]
            }
        ],
        response_format={
            "type": "text"
        },
        temperature=0.5,
        max_completion_tokens=2100
    )

    return {"res": response.choices[0].message.content}