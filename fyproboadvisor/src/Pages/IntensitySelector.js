import React, { useState, useEffect } from 'react';
import './IntensitySelector.css'
function IntensitySelector({ title, updater }) {
  const [low, setLow] = useState("option");
  const [isMed, setIsMed] = useState("option");
  const [isHigh, setIsHigh] = useState("option high");

  // Reset the intensity options when the title changes
  useEffect(() => {
    setLow("option");
    setIsMed("option");
    setIsHigh("option high");
  }, [title]);

  const enterIntensity = (intensity) => {
    // Reset all options
    setLow("option");
    setIsMed("option");
    setIsHigh("option high");

    // Set the selected option
    if (intensity === 'low') {
      setLow('option set-low');
    } else if (intensity === 'med') {
      setIsMed('option set-med');
    } else if (intensity === 'high') {
      setIsHigh('option high set-high');
    }

    // Call the updater function passed as a prop
    updater(intensity);
  };

  return (
    <div>
      <div className='question-header'>
        {title}
      </div>
      <div className='question-option-box'>
        <div className={low} onClick={() => enterIntensity('low')}>
          Low
        </div>
        <div className={isMed} onClick={() => enterIntensity('med')}>
          Medium
        </div>
        <div className={isHigh} onClick={() => enterIntensity('high')}>
          High
        </div>
      </div>
    </div>
  );
};
export default IntensitySelector;
