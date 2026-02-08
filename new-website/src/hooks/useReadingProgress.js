import { useState, useCallback } from 'react';

const STORAGE_KEY = 'readChapters';

function getStoredChapters() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
}

export default function useReadingProgress() {
  const [readChapters, setReadChapters] = useState(getStoredChapters);

  const markAsRead = useCallback((chapterId) => {
    setReadChapters((prev) => {
      if (prev.includes(chapterId)) return prev;
      const updated = [...prev, chapterId];
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
      return updated;
    });
  }, []);

  const isRead = useCallback((chapterId) => {
    return readChapters.includes(chapterId);
  }, [readChapters]);

  return { readChapters, markAsRead, isRead, readCount: readChapters.length };
}
