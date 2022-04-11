import React, { useState } from 'react';

function App() {
    const [selectedFile, setSelectedFile] = useState();

    const [isFilePicked, setIsFilePicked] = useState(false);

    const [operation, setOperation] = useState('encode');

    const [text, setText] = useState('');

    const [decodedText, setDecodedText] = useState('');

    const [errorMsg, setErrorMsg] = useState('');

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
                fetch(
                    `http://localhost:8000/api/${operation}?id=${result.id}&secret_text=${text}`
                )
                    .then((response) => {
                        return operation === 'encode'
                            ? response.blob()
                            : response.json();
                    })
                    .then((result) => {
                        if (operation === 'encode') {
                            // download image
                            const url = window.URL.createObjectURL(result);
                            const a = document.createElement('a');
                            a.style.display = 'none';
                            a.href = url;
                            a.download = 'encoded';
                            document.body.appendChild(a);
                            a.click();
                            window.URL.revokeObjectURL(url);
                            setIsFilePicked(false);
                            setSelectedFile(null);
                            setText('');
                        } else {
                            // display decoded text
                            setDecodedText(result.text);
                        }
                        setErrorMsg('');
                    })
                    .catch((error) => {
                        setErrorMsg(error.message);
                    });
            })
            .catch((error) => {
                setErrorMsg(error.message);
            });
    };

    return (
        <div className="app">
            {errorMsg && <div className="alert alert-danger">{errorMsg}</div>}
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

            <div className="form-group">
                <label htmlFor="operation" id="lbl-operation">
                    Option
                </label>
                <select
                    id="operation"
                    value={operation}
                    onChange={(event) => setOperation(event.target.value)}
                >
                    <option value="encode">Encode</option>
                    <option value="decode">Decode</option>
                </select>
            </div>

            {operation === 'encode' && (
                <textarea
                    placeholder="Type your secret text here"
                    value={text}
                    onChange={(event) => setText(event.target.value)}
                    rows="10"
                    cols="100"
                ></textarea>
            )}

            <div>
                <button onClick={handleSubmission}>Submit</button>
            </div>

            {decodedText && <h5>{decodedText}</h5>}
        </div>
    );
}

export default App;
