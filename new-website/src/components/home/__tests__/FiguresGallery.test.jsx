import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import FiguresGallery from '../FiguresGallery'
import { figures } from '../../../data/figures'

vi.mock('framer-motion', async () => {
  return await import('../../../test/__mocks__/framer-motion.js')
})

describe('FiguresGallery', () => {
  it('renders section with Chinese aria-label by default', () => {
    render(<FiguresGallery />)
    expect(screen.getByLabelText('关键人物展示')).toBeInTheDocument()
  })

  it('renders section with English aria-label when lang=en', () => {
    render(<FiguresGallery lang="en" />)
    expect(screen.getByLabelText('Key Figures Gallery')).toBeInTheDocument()
  })

  it('renders Chinese section title by default', () => {
    render(<FiguresGallery />)
    expect(screen.getByText('👥 关键人物')).toBeInTheDocument()
  })

  it('renders English section title when lang=en', () => {
    render(<FiguresGallery lang="en" />)
    expect(screen.getByText('👥 Key Figures')).toBeInTheDocument()
  })

  it('renders Chinese subtitle by default', () => {
    render(<FiguresGallery />)
    expect(screen.getByText('认识这场货币革命背后的先驱者和传奇人物')).toBeInTheDocument()
  })

  it('renders English subtitle when lang=en', () => {
    render(<FiguresGallery lang="en" />)
    expect(screen.getByText('Meet the pioneers and legends behind this monetary revolution')).toBeInTheDocument()
  })

  it('displays the first figure initially', () => {
    render(<FiguresGallery />)
    const firstFigure = figures[0]
    expect(screen.getByText(firstFigure.name.zh)).toBeInTheDocument()
    expect(screen.getByText(firstFigure.role.zh)).toBeInTheDocument()
    expect(screen.getByText(firstFigure.years)).toBeInTheDocument()
  })

  it('displays figure description and contributions', () => {
    render(<FiguresGallery />)
    const firstFigure = figures[0]
    expect(screen.getByText(firstFigure.description.zh)).toBeInTheDocument()
    firstFigure.contributions.zh.forEach((c) => {
      expect(screen.getByText(c)).toBeInTheDocument()
    })
  })

  it('displays figure quote', () => {
    render(<FiguresGallery />)
    const firstFigure = figures[0]
    expect(screen.getByText(`"${firstFigure.quote.zh}"`)).toBeInTheDocument()
  })

  it('displays counter as 1 / N initially', () => {
    render(<FiguresGallery />)
    expect(screen.getByText(`1 / ${figures.length}`)).toBeInTheDocument()
  })

  it('renders indicator dots for each figure', () => {
    render(<FiguresGallery />)
    const tabs = screen.getAllByRole('tab')
    expect(tabs).toHaveLength(figures.length)
  })

  it('marks the first indicator as selected initially', () => {
    render(<FiguresGallery />)
    const tabs = screen.getAllByRole('tab')
    expect(tabs[0]).toHaveAttribute('aria-selected', 'true')
    expect(tabs[1]).toHaveAttribute('aria-selected', 'false')
  })

  it('renders indicator tablist with proper aria-label', () => {
    render(<FiguresGallery />)
    expect(screen.getByRole('tablist', { name: '人物选择' })).toBeInTheDocument()
  })

  it('renders English tablist aria-label when lang=en', () => {
    render(<FiguresGallery lang="en" />)
    expect(screen.getByRole('tablist', { name: 'Figure selection' })).toBeInTheDocument()
  })

  it('navigates to next figure on next button click', async () => {
    const user = userEvent.setup()
    render(<FiguresGallery />)

    await user.click(screen.getByLabelText('下一位人物'))

    expect(screen.getByText(figures[1].name.zh)).toBeInTheDocument()
    expect(screen.getByText(`2 / ${figures.length}`)).toBeInTheDocument()
  })

  it('navigates to previous figure on prev button click', async () => {
    const user = userEvent.setup()
    render(<FiguresGallery />)

    await user.click(screen.getByLabelText('上一位人物'))

    const lastFigure = figures[figures.length - 1]
    expect(screen.getByText(lastFigure.name.zh)).toBeInTheDocument()
    expect(screen.getByText(`${figures.length} / ${figures.length}`)).toBeInTheDocument()
  })

  it('wraps from last to first on next button click', async () => {
    const user = userEvent.setup()
    render(<FiguresGallery />)

    for (let i = 0; i < figures.length; i++) {
      await user.click(screen.getByLabelText('下一位人物'))
    }

    expect(screen.getByText(figures[0].name.zh)).toBeInTheDocument()
    expect(screen.getByText(`1 / ${figures.length}`)).toBeInTheDocument()
  })

  it('navigates to a specific figure via indicator dot click', async () => {
    const user = userEvent.setup()
    render(<FiguresGallery />)

    const tabs = screen.getAllByRole('tab')
    await user.click(tabs[3])

    expect(screen.getByText(figures[3].name.zh)).toBeInTheDocument()
    expect(tabs[3]).toHaveAttribute('aria-selected', 'true')
    expect(screen.getByText(`4 / ${figures.length}`)).toBeInTheDocument()
  })

  it('updates aria-selected on indicator dots after navigation', async () => {
    const user = userEvent.setup()
    render(<FiguresGallery />)

    await user.click(screen.getByLabelText('下一位人物'))

    const tabs = screen.getAllByRole('tab')
    expect(tabs[0]).toHaveAttribute('aria-selected', 'false')
    expect(tabs[1]).toHaveAttribute('aria-selected', 'true')
  })

  it('renders English navigation button labels when lang=en', () => {
    render(<FiguresGallery lang="en" />)
    expect(screen.getByLabelText('Previous figure')).toBeInTheDocument()
    expect(screen.getByLabelText('Next figure')).toBeInTheDocument()
  })

  it('displays English figure data when lang=en', () => {
    render(<FiguresGallery lang="en" />)
    const firstFigure = figures[0]
    expect(screen.getByText(firstFigure.name.en)).toBeInTheDocument()
    expect(screen.getByText(firstFigure.role.en)).toBeInTheDocument()
  })

  it('renders biography and contributions headings in English', () => {
    render(<FiguresGallery lang="en" />)
    expect(screen.getByText('Biography')).toBeInTheDocument()
    expect(screen.getByText('Key Contributions')).toBeInTheDocument()
  })

  it('renders biography and contributions headings in Chinese', () => {
    render(<FiguresGallery />)
    expect(screen.getByText('简介')).toBeInTheDocument()
    expect(screen.getByText('主要贡献')).toBeInTheDocument()
  })

  it('navigates forward on right swipe (touch)', () => {
    render(<FiguresGallery />)
    const gallery = screen.getByLabelText('关键人物展示').querySelector('[aria-live="polite"]')

    fireEvent.touchStart(gallery, { touches: [{ clientX: 300 }] })
    fireEvent.touchEnd(gallery, { changedTouches: [{ clientX: 200 }] })

    expect(screen.getByText(figures[1].name.zh)).toBeInTheDocument()
  })

  it('navigates backward on left swipe (touch)', () => {
    render(<FiguresGallery />)
    const gallery = screen.getByLabelText('关键人物展示').querySelector('[aria-live="polite"]')

    fireEvent.touchStart(gallery, { touches: [{ clientX: 200 }] })
    fireEvent.touchEnd(gallery, { changedTouches: [{ clientX: 300 }] })

    const lastFigure = figures[figures.length - 1]
    expect(screen.getByText(lastFigure.name.zh)).toBeInTheDocument()
  })

  it('does not navigate on small swipe (< 50px threshold)', () => {
    render(<FiguresGallery />)
    const gallery = screen.getByLabelText('关键人物展示').querySelector('[aria-live="polite"]')

    fireEvent.touchStart(gallery, { touches: [{ clientX: 300 }] })
    fireEvent.touchEnd(gallery, { changedTouches: [{ clientX: 280 }] })

    expect(screen.getByText(figures[0].name.zh)).toBeInTheDocument()
    expect(screen.getByText(`1 / ${figures.length}`)).toBeInTheDocument()
  })

  it('ignores touchEnd without prior touchStart', () => {
    render(<FiguresGallery />)
    const gallery = screen.getByLabelText('关键人物展示').querySelector('[aria-live="polite"]')

    fireEvent.touchEnd(gallery, { changedTouches: [{ clientX: 100 }] })

    expect(screen.getByText(figures[0].name.zh)).toBeInTheDocument()
  })

  it('navigates with ArrowRight key when gallery is visible', () => {
    render(<FiguresGallery />)

    const gallery = document.getElementById('figures') ?? screen.getByLabelText('关键人物展示')
    if (!document.getElementById('figures')) {
      gallery.id = 'figures'
    }
    vi.spyOn(gallery, 'getBoundingClientRect').mockReturnValue({
      top: 0, bottom: 500, left: 0, right: 800, width: 800, height: 500,
    })

    fireEvent.keyDown(window, { key: 'ArrowRight' })

    expect(screen.getByText(figures[1].name.zh)).toBeInTheDocument()
  })

  it('navigates with ArrowLeft key when gallery is visible', () => {
    render(<FiguresGallery />)

    const gallery = document.getElementById('figures') ?? screen.getByLabelText('关键人物展示')
    if (!document.getElementById('figures')) {
      gallery.id = 'figures'
    }
    vi.spyOn(gallery, 'getBoundingClientRect').mockReturnValue({
      top: 0, bottom: 500, left: 0, right: 800, width: 800, height: 500,
    })

    fireEvent.keyDown(window, { key: 'ArrowLeft' })

    const lastFigure = figures[figures.length - 1]
    expect(screen.getByText(lastFigure.name.zh)).toBeInTheDocument()
  })

  it('does not navigate on arrow keys when gallery is not visible', () => {
    render(<FiguresGallery />)

    const gallery = document.getElementById('figures') ?? screen.getByLabelText('关键人物展示')
    if (!document.getElementById('figures')) {
      gallery.id = 'figures'
    }
    vi.spyOn(gallery, 'getBoundingClientRect').mockReturnValue({
      top: -600, bottom: -100, left: 0, right: 800, width: 800, height: 500,
    })

    fireEvent.keyDown(window, { key: 'ArrowRight' })

    expect(screen.getByText(figures[0].name.zh)).toBeInTheDocument()
    expect(screen.getByText(`1 / ${figures.length}`)).toBeInTheDocument()
  })

  it('displays correct emoji for satoshi figure', async () => {
    const user = userEvent.setup()
    render(<FiguresGallery />)

    const satoshiIndex = figures.findIndex((f) => f.id === 'satoshi')
    const tabs = screen.getAllByRole('tab')
    await user.click(tabs[satoshiIndex])

    expect(screen.getByText('🎭')).toBeInTheDocument()
  })

  it('has aria-live="polite" on gallery container', () => {
    render(<FiguresGallery />)
    const liveRegion = screen.getByLabelText('关键人物展示').querySelector('[aria-live="polite"]')
    expect(liveRegion).toBeInTheDocument()
    expect(liveRegion).toHaveAttribute('aria-atomic', 'true')
  })

  it('sets indicator aria-label to figure name', () => {
    render(<FiguresGallery />)
    const tabs = screen.getAllByRole('tab')
    figures.forEach((figure, idx) => {
      expect(tabs[idx]).toHaveAttribute('aria-label', figure.name.zh)
    })
  })

  it('sets indicator aria-label to English name when lang=en', () => {
    render(<FiguresGallery lang="en" />)
    const tabs = screen.getAllByRole('tab')
    figures.forEach((figure, idx) => {
      expect(tabs[idx]).toHaveAttribute('aria-label', figure.name.en)
    })
  })
})
