import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ChapterGrid from '../ChapterGrid'
import { chapters, periods } from '../../../data/chapters'

vi.mock('framer-motion', async () => {
  return await import('../../../test/__mocks__/framer-motion.js')
})

vi.mock('../../common/ShareButtons', () => ({
  ShareButton: () => <button>Share</button>,
}))

describe('ChapterGrid', () => {
  it('renders all chapters by default', () => {
    render(<ChapterGrid lang="zh" />)
    const articles = screen.getAllByRole('article')
    expect(articles.length).toBe(chapters.length)
  })

  it('renders section title in Chinese', () => {
    render(<ChapterGrid lang="zh" />)
    expect(screen.getByText(/章节目录/)).toBeInTheDocument()
  })

  it('renders section title in English', () => {
    render(<ChapterGrid lang="en" />)
    expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent(/Chapters/)
  })

  it('renders period filter buttons', () => {
    render(<ChapterGrid lang="zh" />)
    const buttons = screen.getAllByRole('button')
    const buttonTexts = buttons.map(b => b.textContent)
    expect(buttonTexts).toContain('全部')
    for (const period of periods) {
      expect(buttonTexts.some(t => t.includes(period.name.zh))).toBe(true)
    }
  })

  it('filters chapters by period when clicking filter', async () => {
    const user = userEvent.setup()
    render(<ChapterGrid lang="zh" />)

    const genesisBtn = screen.getByText('创世纪')
    await user.click(genesisBtn)

    const articles = screen.getAllByRole('article')
    expect(articles.length).toBeLessThan(chapters.length)
    expect(articles.length).toBeGreaterThan(0)
  })

  it('shows reading stats when readCount > 0', () => {
    render(<ChapterGrid lang="zh" readCount={5} />)
    expect(screen.getByText(/已读 5/)).toBeInTheDocument()
  })

  it('hides reading stats when readCount is 0', () => {
    render(<ChapterGrid lang="zh" readCount={0} />)
    expect(screen.queryByText(/已读/)).not.toBeInTheDocument()
  })

  it('returns to all chapters when clicking All filter', async () => {
    const user = userEvent.setup()
    render(<ChapterGrid lang="zh" />)

    // Filter first
    await user.click(screen.getByText('创世纪'))
    const filteredCount = screen.getAllByRole('article').length

    // Click All
    await user.click(screen.getByText('全部'))
    const allCount = screen.getAllByRole('article').length

    expect(allCount).toBe(chapters.length)
    expect(allCount).toBeGreaterThan(filteredCount)
  })
})
