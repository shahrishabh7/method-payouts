import React from 'react';
import { useDropzone } from 'react-dropzone';
import Container from '@mui/material/Container';

const getColor = (props) => {
    if (props.isDragAccept) {
        return '#00e676';
    }
    if (props.isDragReject) {
        return '#ff1744';
    }
    if (props.isFocused) {
        return '#2196f3';
    }
    return '#eeeeee';
}

const Dropzone = ({ onDrop, accept }) => {
    // Initializing useDropzone hooks with options
    const { getRootProps, getInputProps, isDragActive, isFocused, isDragReject, isDragAccept } = useDropzone({
        onDrop
    });
    return (
        <Container {...getRootProps(isFocused, isDragAccept, isDragReject)}>
            <input className="dropzone-input" {...getInputProps()} />
            <div className="text-center">
                {isDragActive ? (
                    <p className="dropzone-content">Release to drop the files here</p>
                ) : (
                    <p className="dropzone-content">
                        Upload XML files here
                    </p>
                )}
            </div>
        </Container>
    );
};

export default Dropzone;