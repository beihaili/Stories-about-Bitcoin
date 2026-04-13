import { render, screen, act } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import AchievementToast from '../AchievementToast'

vi.mock('framer-motion', async () => {
  return await import('../../../test/__mocks__/framer-motion.js')
})

const baseAchievement = {
  icon: '🏆',
  name: { zh: '初学者', en: 'Beginner' },
  description: { zh: '完成第一章', en: 'Finish first chapter' },
}

describe('AchievementToast', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    vi.useRealTimers()
  })

  it('renders nothing when achievement is null', () => {
    const { container } = render(
      <AchievementToast achievement={null} onDismiss={vi.fn()} />
    )
    expect(container).toBeEmptyDOMElement()
  })

  it('renders nothing when achievement is undefined', () => {
    const { container } = render(
      <AchievementToast onDismiss={vi.fn()} />
    )
    expect(container).toBeEmptyDOMElement()
  })

  it('renders toast with role alert when achievement is provided', () => {
    render(
      <AchievementToast achievement={baseAchievement} onDismiss={vi.fn()} />
    )
    expect(screen.getByRole('alert')).toBeInTheDocument()
  })

  it('renders achievement icon', () => {
    render(
      <AchievementToast achievement={baseAchievement} onDismiss={vi.fn()} />
    )
    expect(screen.getByText('🏆')).toBeInTheDocument()
  })

  it('renders Chinese unlock label and name by default', () => {
    render(
      <AchievementToast achievement={baseAchievement} onDismiss={vi.fn()} />
    )
    expect(screen.getByText('🎉 成就解锁！')).toBeInTheDocument()
    expect(screen.getByText('初学者')).toBeInTheDocument()
  })

  it('renders Chinese description by default', () => {
    render(
      <AchievementToast achievement={baseAchievement} onDismiss={vi.fn()} />
    )
    expect(screen.getByText('完成第一章')).toBeInTheDocument()
  })

  it('renders English unlock label and name when lang is en', () => {
    render(
      <AchievementToast
        achievement={baseAchievement}
        lang="en"
        onDismiss={vi.fn()}
      />
    )
    expect(screen.getByText('🎉 Achievement Unlocked!')).toBeInTheDocument()
    expect(screen.getByText('Beginner')).toBeInTheDocument()
  })

  it('renders English description when lang is en', () => {
    render(
      <AchievementToast
        achievement={baseAchievement}
        lang="en"
        onDismiss={vi.fn()}
      />
    )
    expect(screen.getByText('Finish first chapter')).toBeInTheDocument()
  })

  it('renders Chinese close button aria-label by default', () => {
    render(
      <AchievementToast achievement={baseAchievement} onDismiss={vi.fn()} />
    )
    expect(screen.getByLabelText('关闭')).toBeInTheDocument()
  })

  it('renders English close button aria-label when lang is en', () => {
    render(
      <AchievementToast
        achievement={baseAchievement}
        lang="en"
        onDismiss={vi.fn()}
      />
    )
    expect(screen.getByLabelText('Close')).toBeInTheDocument()
  })

  it('omits description paragraph when description is missing', () => {
    const achievementWithoutDesc = {
      icon: '⭐',
      name: { zh: '星星', en: 'Star' },
    }
    render(
      <AchievementToast
        achievement={achievementWithoutDesc}
        onDismiss={vi.fn()}
      />
    )
    expect(screen.getByText('星星')).toBeInTheDocument()
    expect(screen.queryByText('完成第一章')).not.toBeInTheDocument()
  })

  it('calls onDismiss when close button is clicked', async () => {
    const onDismiss = vi.fn()
    const user = userEvent.setup()
    render(
      <AchievementToast achievement={baseAchievement} onDismiss={onDismiss} />
    )
    await user.click(screen.getByLabelText('关闭'))
    expect(onDismiss).toHaveBeenCalledTimes(1)
  })

  it('auto-dismisses after 5 seconds', () => {
    vi.useFakeTimers()
    const onDismiss = vi.fn()
    render(
      <AchievementToast achievement={baseAchievement} onDismiss={onDismiss} />
    )
    expect(onDismiss).not.toHaveBeenCalled()
    act(() => {
      vi.advanceTimersByTime(5000)
    })
    expect(onDismiss).toHaveBeenCalledTimes(1)
  })

  it('does not auto-dismiss before 5 seconds elapse', () => {
    vi.useFakeTimers()
    const onDismiss = vi.fn()
    render(
      <AchievementToast achievement={baseAchievement} onDismiss={onDismiss} />
    )
    act(() => {
      vi.advanceTimersByTime(4999)
    })
    expect(onDismiss).not.toHaveBeenCalled()
  })

  it('does not start a timer when achievement is null', () => {
    vi.useFakeTimers()
    const onDismiss = vi.fn()
    render(<AchievementToast achievement={null} onDismiss={onDismiss} />)
    act(() => {
      vi.advanceTimersByTime(10000)
    })
    expect(onDismiss).not.toHaveBeenCalled()
  })

  it('clears the timer on unmount', () => {
    vi.useFakeTimers()
    const onDismiss = vi.fn()
    const { unmount } = render(
      <AchievementToast achievement={baseAchievement} onDismiss={onDismiss} />
    )
    unmount()
    act(() => {
      vi.advanceTimersByTime(5000)
    })
    expect(onDismiss).not.toHaveBeenCalled()
  })

  it('resets the timer when achievement changes', () => {
    vi.useFakeTimers()
    const onDismiss = vi.fn()
    const { rerender } = render(
      <AchievementToast achievement={baseAchievement} onDismiss={onDismiss} />
    )
    act(() => {
      vi.advanceTimersByTime(3000)
    })
    const nextAchievement = {
      icon: '🥇',
      name: { zh: '第二', en: 'Second' },
      description: { zh: '继续', en: 'Continue' },
    }
    rerender(
      <AchievementToast achievement={nextAchievement} onDismiss={onDismiss} />
    )
    act(() => {
      vi.advanceTimersByTime(3000)
    })
    expect(onDismiss).not.toHaveBeenCalled()
    act(() => {
      vi.advanceTimersByTime(2000)
    })
    expect(onDismiss).toHaveBeenCalledTimes(1)
  })
})
