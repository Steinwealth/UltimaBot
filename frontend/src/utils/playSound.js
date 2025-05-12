// frontend/src/utils/playSound.js
import useSoundSettings from '@/hooks/useSoundSettings';

export const playSound = (file, soundMuted = false) => {
  if (soundMuted) return;
  const audio = new Audio(`/sounds/${file}`);
  audio.play();
};
