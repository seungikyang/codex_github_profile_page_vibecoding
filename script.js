const profile = {
  name: "Seo Woo",
  initials: "SW",
  role: "Full-stack Developer",
  availability: "Available for collaboration",
  summary:
    "제품의 흐름을 이해하고, 작은 실험을 안정적인 사용자 경험으로 연결하는 개발자입니다.",
  siteDescription: "제품 감각, 프론트엔드, 자동화 프로젝트를 소개합니다.",
  about:
    "요구사항의 의도를 먼저 정리하고, 인터페이스와 데이터 흐름이 함께 자연스러워지는 방향을 찾습니다. 빠른 프로토타입부터 배포 가능한 결과물까지 직접 손에 잡히는 형태로 만듭니다.",
  contactNote: "프로젝트 협업, 포트폴리오 피드백, 채용 관련 대화를 환영합니다.",
  github: "https://github.com/seoowoo",
  linkedin: "https://www.linkedin.com/in/your-profile",
  email: "hello@example.com",
  stats: [
    { value: "Product", label: "사용자 흐름을 기준으로 우선순위를 정리합니다." },
    { value: "Frontend", label: "반응형 UI와 접근성을 기본값으로 챙깁니다." },
    { value: "Automation", label: "반복 작업을 줄이는 작은 도구를 만듭니다." },
  ],
  signals: [
    { icon: "sparkles", title: "제품 감각", detail: "문제 정의부터 화면 흐름까지" },
    { icon: "monitor-smartphone", title: "반응형 UI", detail: "모바일과 데스크톱 모두 자연스럽게" },
    { icon: "git-branch", title: "배포 경험", detail: "GitHub Pages와 정적 웹사이트" },
    { icon: "shield-check", title: "운영 친화성", detail: "작게 고치고 쉽게 유지하기" },
  ],
  projects: [
    {
      title: "GitHub Pages Portfolio",
      description:
        "개인 소개, 프로젝트, 기술 스택, 연락처를 한 페이지에 담은 정적 포트폴리오 사이트입니다.",
      icon: "layout-dashboard",
      tags: ["HTML", "CSS", "GitHub Pages"],
      link: "https://github.com/seoowoo",
    },
    {
      title: "Product Case Study",
      description:
        "사용자 문제를 가설, 실험, 결과로 나누어 정리하고 다음 개선 방향까지 연결합니다.",
      icon: "line-chart",
      tags: ["UX", "Research", "Iteration"],
      link: "https://github.com/seoowoo",
    },
    {
      title: "Automation Toolkit",
      description:
        "반복되는 개발 및 문서 작업을 줄이기 위한 작은 스크립트와 워크플로우 모음입니다.",
      icon: "workflow",
      tags: ["JavaScript", "CLI", "Docs"],
      link: "https://github.com/seoowoo",
    },
  ],
  stacks: [
    {
      title: "Build",
      icon: "code-2",
      items: [
        ["JavaScript", "UI logic"],
        ["HTML/CSS", "semantic layout"],
        ["GitHub Pages", "static deploy"],
      ],
    },
    {
      title: "Design",
      icon: "palette",
      items: [
        ["Responsive UI", "mobile first"],
        ["Accessibility", "keyboard friendly"],
        ["Information Architecture", "clear structure"],
      ],
    },
    {
      title: "Workflow",
      icon: "terminal-square",
      items: [
        ["Git", "version control"],
        ["Documentation", "decision record"],
        ["Automation", "repeatable tasks"],
      ],
    },
  ],
  timeline: [
    {
      period: "Now",
      title: "Portfolio and public profile",
      description:
        "GitHub Pages 기반의 개인 브랜딩 페이지를 만들고, 작업물을 보기 좋게 정리합니다.",
    },
    {
      period: "Project",
      title: "User-centered web projects",
      description:
        "요구사항을 사용자 흐름으로 바꾸고, 빠른 프로토타입으로 핵심 경험을 검증합니다.",
    },
    {
      period: "Practice",
      title: "Reliable delivery habits",
      description:
        "작은 단위의 커밋, 명확한 문서, 배포 가능한 정적 산출물을 기준으로 작업합니다.",
    },
  ],
};

const setText = (selector, value) => {
  document.querySelectorAll(selector).forEach((element) => {
    element.textContent = value;
  });
};

const setMeta = (selector, value) => {
  const element = document.querySelector(selector);
  if (element) {
    element.setAttribute("content", value);
  }
};

const icon = (name) => `<i data-lucide="${name}" aria-hidden="true"></i>`;

const renderList = (items) => items.map((item) => `<li>${item}</li>`).join("");

function applyProfile() {
  setText('[data-profile="name"]', profile.name);
  setText('[data-profile="initials"]', profile.initials);
  setText('[data-profile="role"]', profile.role);
  setText('[data-profile="availability"]', profile.availability);
  setText('[data-profile="summary"]', profile.summary);
  setText('[data-profile="about"]', profile.about);
  setText('[data-profile="contactNote"]', profile.contactNote);

  document.title = `${profile.name} | Developer Portfolio`;
  setMeta('meta[name="description"]', `${profile.name}의 개발자 포트폴리오. ${profile.siteDescription}`);
  setMeta('meta[property="og:title"]', `${profile.name} | Developer Portfolio`);
  setMeta('meta[property="og:description"]', profile.siteDescription);
  setMeta('meta[name="twitter:title"]', `${profile.name} | Developer Portfolio`);
  setMeta('meta[name="twitter:description"]', profile.siteDescription);
  document.querySelectorAll('[data-link="github"]').forEach((link) => {
    link.href = profile.github;
  });
  document.querySelector('[data-link="linkedin"]').href = profile.linkedin;
  document.querySelector('[data-link="email"]').href = `mailto:${profile.email}`;
  document.querySelector("[data-year]").textContent = new Date().getFullYear();
}

function renderStats() {
  const stats = document.querySelector("#hero-stats");
  stats.innerHTML = profile.stats
    .map(
      (item) => `
        <div>
          <dt>${item.value}</dt>
          <dd>${item.label}</dd>
        </div>
      `,
    )
    .join("");
}

function renderSignals() {
  const signalTrack = document.querySelector("#signal-track");
  signalTrack.innerHTML = profile.signals
    .map(
      (item) => `
        <div class="signal">
          ${icon(item.icon)}
          <p>
            <strong>${item.title}</strong>
            <span>${item.detail}</span>
          </p>
        </div>
      `,
    )
    .join("");
}

function renderProjects() {
  const projectGrid = document.querySelector("#project-grid");
  projectGrid.innerHTML = profile.projects
    .map(
      (project) => `
        <article class="project-card">
          <div class="project-card-header">
            <h3>${project.title}</h3>
            <span class="project-icon">${icon(project.icon)}</span>
          </div>
          <p>${project.description}</p>
          <div>
            <ul class="tag-list">${renderList(project.tags)}</ul>
            <a class="project-link" href="${project.link}" target="_blank" rel="noreferrer">
              자세히 보기
              ${icon("arrow-up-right")}
            </a>
          </div>
        </article>
      `,
    )
    .join("");
}

function renderStacks() {
  const stackGrid = document.querySelector("#stack-grid");
  stackGrid.innerHTML = profile.stacks
    .map(
      (stack) => `
        <article class="stack-card">
          <h3>${icon(stack.icon)}${stack.title}</h3>
          <ul>
            ${stack.items
              .map(([name, detail]) => `<li><strong>${name}</strong><span>${detail}</span></li>`)
              .join("")}
          </ul>
        </article>
      `,
    )
    .join("");
}

function renderTimeline() {
  const timeline = document.querySelector("#timeline");
  timeline.innerHTML = profile.timeline
    .map(
      (item) => `
        <article class="timeline-item">
          <time>${item.period}</time>
          <h3>${item.title}</h3>
          <p>${item.description}</p>
        </article>
      `,
    )
    .join("");
}

function setupHeader() {
  const header = document.querySelector(".site-header");
  const updateHeader = () => {
    header.dataset.elevated = window.scrollY > 8 ? "true" : "false";
  };
  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });
}

function setupMenu() {
  const button = document.querySelector(".menu-toggle");
  const nav = document.querySelector("#mobile-nav");

  const close = () => {
    button.setAttribute("aria-expanded", "false");
    button.setAttribute("aria-label", "메뉴 열기");
    nav.hidden = true;
    document.body.classList.remove("menu-open");
  };

  button.addEventListener("click", () => {
    const isOpen = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!isOpen));
    button.setAttribute("aria-label", isOpen ? "메뉴 열기" : "메뉴 닫기");
    nav.hidden = isOpen;
    document.body.classList.toggle("menu-open", !isOpen);
  });

  nav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", close);
  });

  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      close();
    }
  });
}

applyProfile();
renderStats();
renderSignals();
renderProjects();
renderStacks();
renderTimeline();
setupHeader();
setupMenu();

if (window.lucide) {
  window.lucide.createIcons();
} else {
  window.addEventListener("load", () => window.lucide?.createIcons());
}
