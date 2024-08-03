import React from 'react';

const ImageList = ({ images }) => {
  return (
    <div className="flex flex-wrap justify-center gap-4">
      {images.map((image, index) => (
        <div key={index} className="w-full max-w-sm bg-[#333333] border border-gray-700 rounded-lg shadow mt-5">
          <div className="relative w-full h-0 pb-[70%] overflow-hidden rounded-t-lg">
            <img className="absolute inset-0 w-full h-full object-contain" src={image.image} alt="product image" />
          </div>
          <div className="px-5 pb-5">
            <a href="#">
              <h5 className="text-xl font-semibold tracking-tight text-gray-300 mt-5">{image.prompt}</h5>
            </a>
            <div className="flex items-center justify-between">
              <span className="text-3xl font-bold text-gray-300">{image.style}</span>
              <span className="text-3xl font-bold text-gray-300">{image.color}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default ImageList;



