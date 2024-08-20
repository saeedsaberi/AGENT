import os, re, io, base64, httpx, openai, requests
from .config import  model_config, SAVE_DIR
import matplotlib.pyplot as plt
# import dalle, asyncio
# from dalle import text2im  
from urllib.parse import urljoin


def wikipedia(q):
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]

def calculate(what):
    return eval(what)


def plot(data):
    """
    Plot the given data and return the base64 encoded image.
    The data is expected to be a list of (x, y) tuples.
    """
    # Parse the data assuming it's in the form of a string of tuples
    points = eval(data)  # Example input: "[(1, 2), (2, 3), (3, 4)]"

    # Separate the points into x and y coordinates
    x, y = zip(*points)

    # Create the plot
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title("Generated Plot")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    # Encode the plot as a base64 string
    img_str = base64.b64encode(buf.read()).decode('utf-8')

    # Return the base64 string
    return f"data:image/png;base64,{img_str}"

def plot_schematic(prompt):
    """
    Use GPT-4 to generate a description for a schematic diagram.
    
    Parameters:
    - prompt: str, the initial prompt to instruct GPT-4 on what schematic to create.
    
    Returns:
    - str, the detailed textual description of the schematic.
    """
    response = openai.completions.create(
            model= model_config['default_model'],
            messages=[{"role": "system", "content": "You are an expert in creating schematic descriptions."},
                  {"role": "user", "content": prompt}]
        )
    
    schematic_description = response.choices[0].message.content
    return schematic_description

def generate_schematic_image(description):
    """
    Use DALL-E to generate a schematic image based on a detailed description.
    
    Parameters:
    - description: str, the detailed schematic description from GPT-4.
    
    Returns:
    - image, the generated image from DALL-E or a similar tool.
    """

    client = openai.OpenAI(api_key=openai.api_key)

    response = client.images.generate(
        model   = "dall-e-3",
        prompt  = description,
        size    = "256x256",
        quality = "standard",
        n       = 1,
    )
    image_url = response.data[0].url

    # Get the image content
    image_content = requests.get(image_url).content

    image_path = os.path.join(SAVE_DIR, "generated_image.png")

    # Save the image
    with open(image_path, "wb") as image_file:
        image_file.write(image_content)

    # Return the path to the saved image
    return image_path


def search_internet(query):
    """
    Perform an internet search using the Bing Search API, extract snippets, and summarize them using GPT-4.
    
    Parameters:
    - query: str, the search query
    
    Returns:
    - str, a summary of the search results.
    """
    from .config import api_config  # Importing config when needed
    bing_API_KEY = api_config['bing_API_KEY']
    bing_url = api_config['bing_url']
    
    headers = {"Ocp-Apim-Subscription-Key": bing_API_KEY}
    response = httpx.get(bing_url, params={"q": query}, headers=headers)
    
    if response.status_code == 200:
        search_results = response.json()
        print("DEBUG: search_results JSON:", search_results)  # Debugging line
        
        if 'webPages' in search_results and 'value' in search_results['webPages']:
            snippets = [item.get('snippet', 'No snippet available') for item in search_results['webPages']['value']]
            full_text = "\n".join(snippets)
            
            # Summarize the content using GPT-4
            summary = summarize_with_llm(full_text)
            return summary
        else:
            return "Error: No webPages or value found in search results."
    else:
        return f"Error: Unable to retrieve search results. Status code {response.status_code} - {response.text}"

def summarize_with_llm(text):
    """
    Summarize the given text using GPT-4.
    
    Parameters:
    - text: str, the text to be summarized
    
    Returns:
    - str, the summary of the text.
    """
    response = openai.completions.create(
        model=model_config['default_model'],
        messages=[
            {"role": "system", "content": "You are an expert in summarizing information."},
            {"role": "user", "content": f"Please summarize the following content:\n\n{text}"}
        ]
    )
    summary = response.completion.choices[0].message.content
    return summary


known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "plot": plot,
    "plot_schematic": plot_schematic,
    "generate_schematic_image": generate_schematic_image,
    "search_internet": search_internet, 
}


action_re = re.compile('^Action: (\w+): (.*)$')
