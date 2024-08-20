import httpx
import re, io, base64
import matplotlib.pyplot as plt



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


action_re = re.compile('^Action: (\w+): (.*)$')
