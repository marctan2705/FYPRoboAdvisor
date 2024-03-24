import "./pin.css"
function Pin({image, content}) {
    return ( 
        <div className="pin">
            <img src={image} />
            <div className="pin-content">
                {content}
            </div>
        </div>
     );
}

export default Pin;