import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import LanguageSwitcher from '../LanguageSwitcher'

vi.mock('framer-motion', async () => {
  return await import('../../../test/__mocks__/framer-motion.js')
})

describe('LanguageSwitcher', () => {
  it('renders compact mode with 中 and EN buttons', () => {
    render(<LanguageSwitcher lang="zh" setLang={vi.fn()} isCompact />)
    expect(screen.getByText('中')).toBeInTheDocument()
    expect(screen.getByText('EN')).toBeInTheDocument()
  })

  it('renders full mode with 中文 and English buttons', () => {
    render(<LanguageSwitcher lang="zh" setLang={vi.fn()} />)
    expect(screen.getByText('中文')).toBeInTheDocument()
    expect(screen.getByText('English')).toBeInTheDocument()
  })

  it('calls setLang with en when English button clicked', async () => {
    const user = userEvent.setup()
    const setLang = vi.fn()
    render(<LanguageSwitcher lang="zh" setLang={setLang} isCompact />)
    await user.click(screen.getByText('EN'))
    expect(setLang).toHaveBeenCalledWith('en')
  })

  it('calls setLang with zh when Chinese button clicked', async () => {
    const user = userEvent.setup()
    const setLang = vi.fn()
    render(<LanguageSwitcher lang="en" setLang={setLang} isCompact />)
    await user.click(screen.getByText('中'))
    expect(setLang).toHaveBeenCalledWith('zh')
  })

  it('highlights active language in compact mode', () => {
    const { rerender } = render(<LanguageSwitcher lang="zh" setLang={vi.fn()} isCompact />)
    expect(screen.getByText('中').className).toContain('bg-bitcoin-orange')
    expect(screen.getByText('EN').className).not.toContain('bg-bitcoin-orange')

    rerender(<LanguageSwitcher lang="en" setLang={vi.fn()} isCompact />)
    expect(screen.getByText('EN').className).toContain('bg-bitcoin-orange')
    expect(screen.getByText('中').className).not.toContain('bg-bitcoin-orange')
  })
})
