import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Navbar from '../Navbar'

vi.mock('framer-motion', async () => {
  return await import('../../../test/__mocks__/framer-motion.js')
})

vi.mock('../LanguageSwitcher', () => ({
  default: ({ setLang }) => (
    <div data-testid="lang-switcher">
      <button onClick={() => setLang('zh')}>中</button>
      <button onClick={() => setLang('en')}>EN</button>
    </div>
  ),
}))

describe('Navbar', () => {
  const defaultProps = {
    lang: 'zh',
    setLang: vi.fn(),
    theme: 'light',
    toggleTheme: vi.fn(),
  }

  it('renders Chinese title', () => {
    render(<Navbar {...defaultProps} />)
    expect(screen.getByText('比特币那些事儿')).toBeInTheDocument()
  })

  it('renders English title', () => {
    render(<Navbar {...defaultProps} lang="en" />)
    expect(screen.getByText('Stories about Bitcoin')).toBeInTheDocument()
  })

  it('renders navigation links', () => {
    render(<Navbar {...defaultProps} />)
    expect(screen.getAllByText('时间线').length).toBeGreaterThan(0)
    expect(screen.getAllByText('关键人物').length).toBeGreaterThan(0)
    expect(screen.getAllByText('章节目录').length).toBeGreaterThan(0)
  })

  it('renders GitHub link', () => {
    render(<Navbar {...defaultProps} />)
    const githubLink = screen.getByLabelText('GitHub 仓库')
    expect(githubLink).toHaveAttribute('href', 'https://github.com/beihaili/Stories-about-Bitcoin')
    expect(githubLink).toHaveAttribute('target', '_blank')
  })

  it('renders theme toggle button', () => {
    render(<Navbar {...defaultProps} />)
    const toggleBtns = screen.getAllByLabelText('切换到深色模式')
    expect(toggleBtns.length).toBeGreaterThan(0)
  })

  it('calls toggleTheme on theme button click', async () => {
    const user = userEvent.setup()
    render(<Navbar {...defaultProps} />)
    const toggleBtns = screen.getAllByLabelText('切换到深色模式')
    await user.click(toggleBtns[0])
    expect(defaultProps.toggleTheme).toHaveBeenCalled()
  })

  it('toggles mobile menu on click', async () => {
    const user = userEvent.setup()
    render(<Navbar {...defaultProps} />)
    const menuBtn = screen.getByLabelText('切换菜单')
    expect(menuBtn).toHaveAttribute('aria-expanded', 'false')
    await user.click(menuBtn)
    // After click, the mobile menu content should appear
    expect(screen.getAllByText('时间线').length).toBeGreaterThanOrEqual(2)
  })

  it('renders start reading link with correct URL', () => {
    render(<Navbar {...defaultProps} />)
    const readLinks = screen.getAllByText('开始阅读')
    const link = readLinks.find(el => el.closest('a'))
    expect(link.closest('a')).toHaveAttribute('href', 'https://beihaili.github.io/Stories-about-Bitcoin/zh/')
  })
})
