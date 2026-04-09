import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, act } from '@testing-library/react';

vi.mock('framer-motion', async () => {
  return await import('../../../test/__mocks__/framer-motion.js');
});

import AchievementToast from '../AchievementToast';

const mockAchievement = {
  icon: '🏆',
  name: { zh: '测试成就', en: 'Test Achievement' },
  description: { zh: '测试描述', en: 'Test description' },
};

const mockAchievementNoDesc = {
  icon: '⭐',
  name: { zh: '无描述成就', en: 'No Desc Achievement' },
};

describe('AchievementToast', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('renders nothing when achievement is null', () => {
    const { container } = render(
      <AchievementToast achievement={null} onDismiss={vi.fn()} />
    );
    expect(container.querySelector('[role="alert"]')).toBeNull();
  });

  it('renders nothing when achievement is undefined', () => {
    const { container } = render(
      <AchievementToast onDismiss={vi.fn()} />
    );
    expect(container.querySelector('[role="alert"]')).toBeNull();
  });

  it('renders achievement toast when achievement is provided', () => {
    render(
      <AchievementToast achievement={mockAchievement} onDismiss={vi.fn()} />
    );
    expect(screen.getByRole('alert')).toBeInTheDocument();
    expect(screen.getByText('🏆')).toBeInTheDocument();
    expect(screen.getByText('测试成就')).toBeInTheDocument();
    expect(screen.getByText('测试描述')).toBeInTheDocument();
  });

  it('displays Chinese text by default (lang="zh")', () => {
    render(
      <AchievementToast achievement={mockAchievement} onDismiss={vi.fn()} />
    );
    expect(screen.getByText('🎉 成就解锁！')).toBeInTheDocument();
    expect(screen.getByText('测试成就')).toBeInTheDocument();
    expect(screen.getByText('测试描述')).toBeInTheDocument();
    expect(screen.getByLabelText('关闭')).toBeInTheDocument();
  });

  it('displays English text when lang="en"', () => {
    render(
      <AchievementToast achievement={mockAchievement} lang="en" onDismiss={vi.fn()} />
    );
    expect(screen.getByText('🎉 Achievement Unlocked!')).toBeInTheDocument();
    expect(screen.getByText('Test Achievement')).toBeInTheDocument();
    expect(screen.getByText('Test description')).toBeInTheDocument();
    expect(screen.getByLabelText('Close')).toBeInTheDocument();
  });

  it('does not render description when achievement has no description', () => {
    render(
      <AchievementToast achievement={mockAchievementNoDesc} onDismiss={vi.fn()} />
    );
    expect(screen.getByText('⭐')).toBeInTheDocument();
    expect(screen.getByText('无描述成就')).toBeInTheDocument();
    expect(screen.queryByText('测试描述')).toBeNull();
  });

  it('calls onDismiss when close button is clicked', () => {
    const onDismiss = vi.fn();
    render(
      <AchievementToast achievement={mockAchievement} onDismiss={onDismiss} />
    );
    fireEvent.click(screen.getByLabelText('关闭'));
    expect(onDismiss).toHaveBeenCalledTimes(1);
  });

  it('auto-dismisses after 5 seconds', () => {
    const onDismiss = vi.fn();
    render(
      <AchievementToast achievement={mockAchievement} onDismiss={onDismiss} />
    );
    expect(onDismiss).not.toHaveBeenCalled();
    act(() => {
      vi.advanceTimersByTime(5000);
    });
    expect(onDismiss).toHaveBeenCalledTimes(1);
  });

  it('does not auto-dismiss before 5 seconds', () => {
    const onDismiss = vi.fn();
    render(
      <AchievementToast achievement={mockAchievement} onDismiss={onDismiss} />
    );
    act(() => {
      vi.advanceTimersByTime(4999);
    });
    expect(onDismiss).not.toHaveBeenCalled();
  });

  it('clears timer on unmount before auto-dismiss fires', () => {
    const onDismiss = vi.fn();
    const { unmount } = render(
      <AchievementToast achievement={mockAchievement} onDismiss={onDismiss} />
    );
    act(() => {
      vi.advanceTimersByTime(2000);
    });
    unmount();
    act(() => {
      vi.advanceTimersByTime(5000);
    });
    expect(onDismiss).not.toHaveBeenCalled();
  });

  it('does not set timer when achievement is null', () => {
    const onDismiss = vi.fn();
    render(
      <AchievementToast achievement={null} onDismiss={onDismiss} />
    );
    act(() => {
      vi.advanceTimersByTime(10000);
    });
    expect(onDismiss).not.toHaveBeenCalled();
  });

  it('resets timer when achievement changes', () => {
    const onDismiss = vi.fn();
    const { rerender } = render(
      <AchievementToast achievement={mockAchievement} onDismiss={onDismiss} />
    );
    act(() => {
      vi.advanceTimersByTime(3000);
    });
    const newAchievement = {
      icon: '🎯',
      name: { zh: '新成就', en: 'New Achievement' },
      description: { zh: '新描述', en: 'New description' },
    };
    rerender(
      <AchievementToast achievement={newAchievement} onDismiss={onDismiss} />
    );
    act(() => {
      vi.advanceTimersByTime(3000);
    });
    expect(onDismiss).not.toHaveBeenCalled();
    act(() => {
      vi.advanceTimersByTime(2000);
    });
    expect(onDismiss).toHaveBeenCalledTimes(1);
  });

  it('renders the close button with × character', () => {
    render(
      <AchievementToast achievement={mockAchievement} onDismiss={vi.fn()} />
    );
    const closeButton = screen.getByLabelText('关闭');
    expect(closeButton.textContent).toBe('×');
  });

  it('has role="alert" on the toast container', () => {
    render(
      <AchievementToast achievement={mockAchievement} onDismiss={vi.fn()} />
    );
    expect(screen.getByRole('alert')).toBeInTheDocument();
  });
});
