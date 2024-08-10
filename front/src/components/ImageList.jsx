import React from 'react';
import anime_icon from '../assets/icons/anime.png';
import cnm_icon from '../assets/icons/cnm.png';
import goth_icon from '../assets/icons/goth.png';
import minim_icon from '../assets/icons/minim.png';
import sci_icon from '../assets/icons/sci.png';

const ImageList = ({ images }) => {
  const styles = [
    { value: 'AN', label: 'Anime', icon: anime_icon },
    { value: 'GOTH', label: 'Gothic', icon: goth_icon },
    { value: 'Sci-Fi', label: 'Sci-Fi', icon: sci_icon },
    { value: 'CNM', label: 'Cinematic', icon: cnm_icon },
    { value: 'MN', label: 'Minimalistic', icon: minim_icon }
  ];

  const colors = [
    { value: 'BW', label: 'Black and white', colorCode: ['#000000', '#999'] }, // Two colors for BW
    { value: 'Yel', label: 'Yellow', colorCode: ['#FFFF00'] },
    { value: 'br', label: 'Bright', colorCode: ['#FF5733'] },
    { value: 'dr', label: 'Dark and gloomy', colorCode: ['#4A4A4A'] },
    { value: 'pl', label: 'Pastel colors', colorCode: ['#FFB6C1'] }
  ];

  return (
    <div className="flex flex-wrap justify-center gap-4">
      {images.map((image, index) => {
        const style = styles.find(s => s.value === image.style);
        const color = colors.find(c => c.value === image.color);

        return (
          <div key={index} className="w-full max-w-sm bg-[#333333] border border-gray-700 rounded-lg shadow mt-5">
            <div className="relative w-full h-0 pb-[70%] overflow-hidden rounded-t-lg">
              <img className="absolute inset-0 w-full h-full object-contain" src={image.image} alt="product image" />
            </div>
            <div className="px-5 pb-5">
              <a href="#">
                <h5 className="text-xl font-semibold tracking-tight text-gray-300 mt-5">{image.prompt}</h5>
              </a>
              <div className="flex items-center justify-between">
                {/* Style */}
                <div className="flex items-center">
                  {style && (
                    <>
                      <img src={style.icon} alt={style.label} className="w-6 h-6 mr-2" />
                      <span className="text-lg font-bold text-gray-300">{style.label}</span>
                    </>
                  )}
                </div>
                {/* Color */}
                <div className="flex items-center">
                  {color && color.colorCode.map((c, i) => (
                    <span key={i} className="w-6 h-6 mr-2 rounded-full" style={{ backgroundColor: c }}></span>
                  ))}
                  {color && <span className="text-lg font-bold text-gray-300">{color.label}</span>}
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default ImageList;



