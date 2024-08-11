import React from 'react';

const Developer = () => {
  return (
    <div className="developer-wrapper bg-lime-400 p-4 rounded-full ">
      <h5 className="text-center mb-4 text-base font-medium leading-tight text-gray-800 md:text-lg lg:text-lg dark:text-gray-300">
        Website was developed by{' '}
        <a
          href="https://www.instagram.com/codium_123"
          className="underline underline-offset-4 decoration-blue-500 hover:decoration-blue-700 transition duration-300"
        >
          Michael Shpilevsky
        </a>
      </h5>
    </div>
  );
}

export default Developer;
