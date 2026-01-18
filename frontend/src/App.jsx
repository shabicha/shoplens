import { useState } from 'react';
import Upload from './Upload';
import Card from './Card';

function App() {
  const [results, setResults] = useState([]);

  const handleResults = (data) => {
    setResults(data.results || []);
  };

  const hasResults = results.length > 0;

  return (
    <>
      {/* Upload positioning layer */}
      <div
        className={
          hasResults
            ? "fixed top-6 left-6 z-50 transition-all duration-300"
            : "fixed inset-0 flex items-center justify-center z-50 transition-all duration-300"
        }
      >
        <Upload onResults={handleResults} />
      </div>

      {/* Cards */}
      {hasResults && (
        <div className="pt-32 px-6">
          <div className="grid grid-cols-4 gap-6">
            {results.map((result, index) => (
              <Card
                key={index}
                imageUrl={result.image_url}
                productName={result.product_name}
                price={result.price}
                productUrl={result.product_url}
                similarityScore={result.similarity_score}
              />
            ))}
          </div>
        </div>
      )}
    </>
  );
}

export default App;
