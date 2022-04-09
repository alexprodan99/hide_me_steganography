import React, { useEffect, useState } from 'react';

function App() {
    const [selectedFile, setSelectedFile] = useState();

    const [isFilePicked, setIsFilePicked] = useState(false);

    const changeHandler = (event) => {
        setSelectedFile(event.target.files[0]);

        setIsFilePicked(true);
    };

    const handleSubmission = () => {
        const formData = new FormData();

        formData.append('file', selectedFile);

        fetch(
            'http://localhost:8000/api/upload',

            {
                method: 'POST',

                body: formData,
            }
        )
            .then((response) => response.json())

            .then((result) => {
                console.log('Success:', result);
                setIsFilePicked(false);
                setSelectedFile(null);
            })

            .catch((error) => {
                console.error('Error:', error);
            });
    };

    return (
        <div style={{ textAlign: 'center' }}>
            <input type="file" name="file" onChange={changeHandler} />

            {isFilePicked ? (
                <div>
                    <p>Filename: {selectedFile.name}</p>

                    <p>Filetype: {selectedFile.type}</p>

                    <p>Size in bytes: {selectedFile.size}</p>

                    <p>
                        lastModifiedDate:{' '}
                        {new Date(
                            selectedFile.lastModified
                        ).toLocaleDateString()}
                    </p>
                </div>
            ) : (
                <p>Select a file to show details</p>
            )}

            <div>
                <button onClick={handleSubmission}>Submit</button>
            </div>
        </div>
    );
}

export default App;
