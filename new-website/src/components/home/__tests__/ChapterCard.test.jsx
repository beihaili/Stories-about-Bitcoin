import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ChapterCard from '../ChapterCard'

vi.mock('framer-motion', async () => {
  return await import('../../../test/__mocks__/framer-motion.js')
})

vi.mock('../../common/ShareButtons', () => ({
  ShareButton: () => <button>Share</button>,
}))

const mockChapter = {
  id: 1,
  title: { zh: '创世区块', en: 'Genesis Block' },
  summary: { zh: '中本聪的故事', en: 'The story of Satoshi' },
  icon: '🔥',
  year: '2009',
  readingTime: 15,
  link: { zh: '/zh/ch01.html', en: '/en/ch01.html' },
}

describe('ChapterCard', () => {
  it('renders chapter title in Chinese', () => {
    render(<ChapterCard chapter={mockChapter} lang="zh" index={0} />)
    expect(screen.getByText('创世区块')).toBeInTheDocument()
  })

  it('renders chapter title in English', () => {
    render(<ChapterCard chapter={mockChapter} lang="en" index={0} />)
    expect(screen.getByText('Genesis Block')).toBeInTheDocument()
  })

  it('renders summary text', () => {
    render(<ChapterCard chapter={mockChapter} lang="zh" index={0} />)
    expect(screen.getAllByText('中本聪的故事').length).toBeGreaterThan(0)
  })

  it('renders year badge', () => {
    render(<ChapterCard chapter={mockChapter} lang="zh" index={0} />)
    expect(screen.getByText('2009')).toBeInTheDocument()
  })

  it('renders reading time', () => {
    render(<ChapterCard chapter={mockChapter} lang="zh" index={0} />)
    expect(screen.getByText(/15.*分钟/)).toBeInTheDocument()
  })

  it('shows read badge when isRead is true', () => {
    render(<ChapterCard chapter={mockChapter} lang="zh" index={0} isRead={true} />)
    expect(screen.getByText('已读')).toBeInTheDocument()
  })

  it('does not show read badge when isRead is false', () => {
    render(<ChapterCard chapter={mockChapter} lang="zh" index={0} isRead={false} />)
    expect(screen.queryByText('已读')).not.toBeInTheDocument()
  })

  it('calls markAsRead and window.open on click', async () => {
    const windowOpen = vi.spyOn(window, 'open').mockImplementation(() => {})
    const markAsRead = vi.fn()

    const { container } = render(
      <ChapterCard chapter={mockChapter} lang="zh" index={0} markAsRead={markAsRead} />
    )

    container.querySelector('[role="article"]').click()
    expect(windowOpen).toHaveBeenCalledWith(
      expect.stringContaining('/zh/ch01.html'),
      '_blank'
    )
    expect(markAsRead).toHaveBeenCalledWith(1)
    windowOpen.mockRestore()
  })

  it('opens chapter link on Enter key', async () => {
    const windowOpen = vi.spyOn(window, 'open').mockImplementation(() => {})
    const user = userEvent.setup()

    render(<ChapterCard chapter={mockChapter} lang="zh" index={0} />)

    const card = screen.getByRole('article')
    card.focus()
    await user.keyboard('{Enter}')
    expect(windowOpen).toHaveBeenCalled()
    windowOpen.mockRestore()
  })

  it('has proper aria-label', () => {
    render(<ChapterCard chapter={mockChapter} lang="zh" index={0} />)
    expect(screen.getByRole('article')).toHaveAttribute('aria-label', '第1章：创世区块')
  })
})
