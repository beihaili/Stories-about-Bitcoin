import { useState, useCallback, useMemo } from 'react';

const STORAGE_KEY = 'achievements';

const MILESTONES = [
  { id: 'starter', threshold: 1, name: { zh: '启程者', en: 'Starter' }, icon: '🚀', description: { zh: '阅读第 1 章', en: 'Read your first chapter' } },
  { id: 'explorer', threshold: 5, name: { zh: '探索者', en: 'Explorer' }, icon: '🧭', description: { zh: '阅读 5 章', en: 'Read 5 chapters' } },
  { id: 'scholar', threshold: 10, name: { zh: '学者', en: 'Scholar' }, icon: '📚', description: { zh: '阅读 10 章', en: 'Read 10 chapters' } },
  { id: 'master', threshold: 20, name: { zh: '大师', en: 'Master' }, icon: '🎓', description: { zh: '阅读 20 章', en: 'Read 20 chapters' } },
  { id: 'completionist', threshold: 33, name: { zh: '完成者', en: 'Completionist' }, icon: '👑', description: { zh: '阅读全部章节', en: 'Read all chapters' } },
];

const PERIOD_BADGES = [
  { id: 'badge-prologue', period: 'prologue', chapterIds: [0], name: { zh: '序章通关', en: 'Prologue Complete' }, icon: '📖' },
  { id: 'badge-genesis', period: 'genesis', chapterIds: [1, 2, 3, 4, 5], name: { zh: '创世纪通关', en: 'Genesis Complete' }, icon: '🔮' },
  { id: 'badge-first-steps', period: 'first-steps', chapterIds: [6, 7, 8, 9, 10], name: { zh: '初出茅庐通关', en: 'First Steps Complete' }, icon: '👤' },
  { id: 'badge-rising-storm', period: 'rising-storm', chapterIds: [11, 12, 13, 14, 15], name: { zh: '风起云涌通关', en: 'Rising Storm Complete' }, icon: '⚔️' },
  { id: 'badge-undercurrents', period: 'undercurrents', chapterIds: [16, 17, 18, 19, 20, 21], name: { zh: '暗潮汹涌通关', en: 'Undercurrents Complete' }, icon: '🌊' },
  { id: 'badge-breaking-waves', period: 'breaking-waves', chapterIds: [22, 23, 24, 25, 26, 27], name: { zh: '破浪前行通关', en: 'Breaking Waves Complete' }, icon: '🏄' },
  { id: 'badge-future-promise', period: 'future-promise', chapterIds: [28, 29, 30, 31, 32], name: { zh: '未来可期通关', en: 'Future Promise Complete' }, icon: '🌟' },
  { id: 'badge-special', period: 'special', chapterIds: [33], name: { zh: '特别篇通关', en: 'Special Complete' }, icon: '💐' },
];

const ALL_ACHIEVEMENTS = [...MILESTONES, ...PERIOD_BADGES];

function getStoredAchievements() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
}

function computeUnlocked(readChapters) {
  const readSet = new Set(readChapters);
  const unlocked = [];

  for (const m of MILESTONES) {
    if (readChapters.length >= m.threshold) {
      unlocked.push(m.id);
    }
  }

  for (const b of PERIOD_BADGES) {
    if (b.chapterIds.every(id => readSet.has(id))) {
      unlocked.push(b.id);
    }
  }

  return unlocked;
}

export default function useAchievements(readChapters = []) {
  const [shownIds, setShownIds] = useState(getStoredAchievements);
  const [newAchievement, setNewAchievement] = useState(null);

  // Derive currently unlocked achievements from readChapters
  const unlockedIds = useMemo(() => computeUnlocked(readChapters), [readChapters]);

  // Check for newly unlocked achievements that haven't been shown yet
  const checkAndNotify = useCallback(() => {
    const newlyUnlocked = unlockedIds.filter(id => !shownIds.includes(id));
    if (newlyUnlocked.length > 0) {
      const updated = [...shownIds, ...newlyUnlocked];
      setShownIds(updated);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
      const achievement = ALL_ACHIEVEMENTS.find(a => a.id === newlyUnlocked[0]);
      setNewAchievement(achievement);
    }
  }, [unlockedIds, shownIds]);

  // Called from markAsRead handler (event-driven, not effect-driven)
  // We expose this so App can call it after marking a chapter as read
  const onChapterRead = useCallback(() => {
    // Use a microtask to run after state updates settle
    queueMicrotask(checkAndNotify);
  }, [checkAndNotify]);

  const dismissAchievement = useCallback(() => {
    setNewAchievement(null);
  }, []);

  const isPeriodComplete = useCallback((periodId) => {
    const badge = PERIOD_BADGES.find(b => b.period === periodId);
    if (!badge) return false;
    const readSet = new Set(readChapters);
    return badge.chapterIds.every(id => readSet.has(id));
  }, [readChapters]);

  return {
    unlockedIds,
    unlockedCount: unlockedIds.length,
    totalCount: ALL_ACHIEVEMENTS.length,
    newAchievement,
    dismissAchievement,
    isPeriodComplete,
    onChapterRead,
    allAchievements: ALL_ACHIEVEMENTS,
  };
}
