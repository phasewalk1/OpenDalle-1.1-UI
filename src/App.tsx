import { useState } from 'react';
import './App.css';

function App() {
  const [description, setDescription] = useState('');
  const [generatedImage, setGeneratedImage] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const generateImage = async () => {
    setIsGenerating(true);
    console.log("Using prompt: " + description)
    const response = await fetch('http://localhost:8000/generate-image', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ description }),
    });

    const data = await response.json();
    setGeneratedImage(data.image);
    setIsGenerating(false);
    console.log("Generated image: " + data.image)
  };

  return (
    <>
      <div>
        {/* Existing code for logos */}
      </div>
      <h1>Text-to-Image with DALL-E</h1>
      <div className="image-generator">
        <input
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Describe the image..."
        />
        <button onClick={generateImage} disabled={isGenerating}>Generate Image</button>
        {isGenerating && <p>Generating image...</p>}
        {generatedImage && <img src={`data:image/jpeg;base64,${generatedImage}`} alt="Generated" />}
      </div>
    </>
  );
}

export default App;
