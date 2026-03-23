document.addEventListener('DOMContentLoaded', () => {
  const elements = document.querySelectorAll('.reveal');

  const reveal = () => {
    const trigger = window.innerHeight * 0.9;
    elements.forEach((element) => {
      if (element.getBoundingClientRect().top < trigger) {
        element.classList.add('active');
      }
    });
  };

  reveal();
  window.addEventListener('scroll', reveal);
});
