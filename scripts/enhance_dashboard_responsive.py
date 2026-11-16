#!/usr/bin/env python3
"""
Inject Mobile & Cross-device Responsive Styling into public/dashboard.html and root dashboard.html.
"""

import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\User\.gemini\antigravity\scratch\roar-word-replica")
PUBLIC_DASHBOARD = ROOT / "public" / "dashboard.html"
ROOT_DASHBOARD = ROOT / "dashboard.html"

RESPONSIVE_CSS = """
    /* ====== CROSS-DEVICE RESPONSIVE SUITE (Mobile, Tablet, Desktop) ====== */
    
    /* Smooth touch interactions and horizontal nav scrolling */
    .nav-tabs {
      display: flex;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: thin;
      scrollbar-color: var(--card-border) transparent;
      gap: 0.5rem;
      padding-bottom: 2px;
    }
    .nav-tab {
      white-space: nowrap;
      flex-shrink: 0;
      touch-action: manipulation;
    }
    
    /* Ensure table container scrolls cleanly on small screens */
    .table-container {
      width: 100%;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      border-radius: 8px;
    }

    /* Modal mobile friendliness */
    .modal {
      max-height: 90vh;
      overflow-y: auto;
      -webkit-overflow-scrolling: touch;
    }

    /* Tablet breakpoint (<= 1024px) */
    @media (max-width: 1024px) {
      .app-container {
        padding: 1.25rem 1rem;
      }
      .metrics-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 1rem !important;
      }
    }

    /* Mobile landscape and tablet portrait (<= 768px) */
    @media (max-width: 768px) {
      .app-header {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 1rem !important;
        padding: 1rem !important;
      }
      .brand {
        justify-content: flex-start;
      }
      .header-actions {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 0.5rem !important;
        width: 100% !important;
      }
      .header-actions .btn {
        flex: 1 1 calc(50% - 0.5rem) !important;
        min-height: 44px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
      }
      .card-header {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 0.75rem !important;
      }
      .card-actions, .filter-group {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 0.5rem !important;
        width: 100% !important;
      }
      .card-actions .btn,
      .card-actions .form-control {
        flex: 1 1 100% !important;
        min-height: 44px !important;
      }
      .form-row {
        flex-direction: column !important;
        gap: 0.75rem !important;
      }
      .form-group {
        width: 100% !important;
      }
      table {
        min-width: 580px !important;
      }
      .modal {
        width: 95vw !important;
        max-width: 95vw !important;
        padding: 1.25rem 1rem !important;
      }
      .session-pills {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 0.5rem !important;
      }
      .session-pill {
        flex: 1 1 calc(33.33% - 0.5rem) !important;
        min-width: 85px !important;
        text-align: center !important;
        padding: 0.6rem 0.4rem !important;
      }
    }

    /* Small Phone Screens (<= 480px) */
    @media (max-width: 480px) {
      .app-container {
        padding: 0.75rem 0.5rem !important;
      }
      .metrics-grid {
        grid-template-columns: 1fr !important;
      }
      .metric-card {
        padding: 1rem !important;
      }
      .metric-value {
        font-size: 1.75rem !important;
      }
      .header-actions .btn {
        flex: 1 1 100% !important;
      }
      .session-pill {
        flex: 1 1 calc(50% - 0.5rem) !important;
      }
      .btn {
        padding: 0.65rem 1rem !important;
        font-size: 0.875rem !important;
      }
    }
"""

def enhance_dashboard():
    print(f"Reading {PUBLIC_DASHBOARD}...")
    txt = PUBLIC_DASHBOARD.read_text(encoding='utf-8')
    
    # Check if responsive CSS already added
    if "CROSS-DEVICE RESPONSIVE SUITE" in txt:
        print("Responsive CSS already present, updating...")
        # Replace existing block
        start_idx = txt.find("/* ====== CROSS-DEVICE RESPONSIVE SUITE")
        end_idx = txt.find("</style>", start_idx)
        txt = txt[:start_idx] + RESPONSIVE_CSS.strip() + "\n  " + txt[end_idx:]
    else:
        print("Injecting responsive CSS before </style>...")
        idx = txt.find("</style>")
        if idx == -1:
            print("❌ </style> not found!")
            return False
        txt = txt[:idx] + RESPONSIVE_CSS + "  " + txt[idx:]
    
    PUBLIC_DASHBOARD.write_text(txt, encoding='utf-8')
    shutil.copy2(PUBLIC_DASHBOARD, ROOT_DASHBOARD)
    print(f"✅ Enhanced dashboard.html in public/ and root!")
    return True

if __name__ == '__main__':
    enhance_dashboard()
