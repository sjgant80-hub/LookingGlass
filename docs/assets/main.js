// LookingGlass - Konomi Systems
document.addEventListener('DOMContentLoaded', () => {
  console.log('LookingGlass v0.1.0 - Konomi Systems');
  document.querySelectorAll('.card').forEach(card => {
    card.style.cursor = 'pointer';
    card.addEventListener('mouseenter', () => {
      card.style.borderColor = '#00cccc';
    });
    card.addEventListener('mouseleave', () => {
      card.style.borderColor = '#2a2a3a';
    });
  });
});
