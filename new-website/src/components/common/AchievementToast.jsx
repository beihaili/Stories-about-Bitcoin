import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const AchievementToast = ({ achievement, lang = 'zh', onDismiss }) => {
  useEffect(() => {
    if (achievement) {
      const timer = setTimeout(onDismiss, 5000);
      return () => clearTimeout(timer);
    }
  }, [achievement, onDismiss]);

  return (
    <AnimatePresence>
      {achievement && (
        <motion.div
          role="alert"
          className="fixed bottom-20 right-6 z-50 bg-gradient-to-r from-bitcoin-orange to-bitcoin-gold text-white rounded-xl shadow-2xl p-4 max-w-xs"
          initial={{ opacity: 0, x: 100, scale: 0.8 }}
          animate={{ opacity: 1, x: 0, scale: 1 }}
          exit={{ opacity: 0, x: 100, scale: 0.8 }}
          transition={{ type: 'spring', damping: 20, stiffness: 300 }}
        >
          <div className="flex items-start gap-3">
            <span className="text-3xl">{achievement.icon}</span>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium opacity-90">
                {lang === 'zh' ? '🎉 成就解锁！' : '🎉 Achievement Unlocked!'}
              </p>
              <p className="font-bold text-sm mt-0.5">{achievement.name[lang]}</p>
              {achievement.description && (
                <p className="text-xs opacity-80 mt-0.5">{achievement.description[lang]}</p>
              )}
            </div>
            <button
              onClick={onDismiss}
              className="text-white/70 hover:text-white text-lg leading-none"
              aria-label={lang === 'zh' ? '关闭' : 'Close'}
            >
              ×
            </button>
          </div>
          {/* Auto-dismiss progress bar */}
          <motion.div
            className="absolute bottom-0 left-0 h-1 bg-white/30 rounded-b-xl"
            initial={{ width: '100%' }}
            animate={{ width: '0%' }}
            transition={{ duration: 5, ease: 'linear' }}
          />
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default AchievementToast;
