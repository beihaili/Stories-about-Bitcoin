import { useState, useCallback } from 'react';

const STORAGE_KEY = 'bookmarkedChapters';

function getStoredBookmarks() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
}

export default function useBookmarks() {
  const [bookmarks, setBookmarks] = useState(getStoredBookmarks);

  const toggleBookmark = useCallback((chapterId) => {
    setBookmarks((prev) => {
      const updated = prev.includes(chapterId)
        ? prev.filter(id => id !== chapterId)
        : [...prev, chapterId];
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
      return updated;
    });
  }, []);

  const isBookmarked = useCallback((chapterId) => {
    return bookmarks.includes(chapterId);
  }, [bookmarks]);

  return { bookmarks, toggleBookmark, isBookmarked, bookmarkCount: bookmarks.length };
}
