import "./queryrec.css"

function QueryRec({Query, onClick}) {
    return ( 
        <div className="querycard" onClick={() => onClick(Query)}>
            {Query}
        </div>
     );
}

export default QueryRec;