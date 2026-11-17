from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import PageBreak, SimpleDocTemplate, Paragraph, Spacer, Preformatted, ListFlowable, ListItem

def build(path):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=18*mm, bottomMargin=16*mm,
                            title="Modern Fortran - Developer Quick Reference", author="FORTLS.com")
    h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=20, leading=24, spaceAfter=4)
    h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=12.5, leading=16, spaceBefore=11, spaceAfter=4, textColor=colors.HexColor("#273244"))
    p = ParagraphStyle("p", fontName="Helvetica", fontSize=10, leading=14)
    code = ParagraphStyle("c", fontName="Courier", fontSize=9.5, leading=12.5, backColor=colors.HexColor("#f1f3f6"), borderPadding=6, spaceBefore=4, spaceAfter=6)
    small = ParagraphStyle("s", parent=p, fontSize=8.5, leading=11, textColor=colors.HexColor("#555555"))
    def bl(items): return ListFlowable([ListItem(Paragraph(i, p), leftIndent=12) for i in items], bulletType="bullet", start="-", leftIndent=12)
    s = [Paragraph("Modern Fortran - Developer Quick Reference", h1),
         Paragraph("A compact orientation sheet for developers working with modern Fortran. Check compiler and project documentation for version-specific behavior.", p),
         Paragraph("Core source structure", h2),
         Preformatted("program main\n  implicit none\n  print *, 'Hello, Fortran!'\nend program main", code),
         Paragraph("Useful language habits", h2),
         bl(["Use <font face='Courier'>implicit none</font> in program units to avoid unintended implicit typing.",
             "Prefer <font face='Courier'>iso_fortran_env</font> kinds such as <font face='Courier'>real64</font> when a specific precision is required.",
             "Use modules to organize reusable procedures, derived types and shared interfaces.",
             "Use <font face='Courier'>allocatable</font> for dynamically sized data when ownership and lifetime are clear.",
             "Check array bounds, <font face='Courier'>intent</font> attributes and I/O status (<font face='Courier'>iostat</font>) in robust code."]),
         Paragraph("Build and package workflow", h2),
         Paragraph("Use the documentation of your selected compiler. For package-oriented projects, explore fpm (Fortran Package Manager). Keep build instructions reproducible and record compiler versions.", p),
         Preformatted("fpm new my_project   # create a project\nfpm build            # compile\nfpm run              # run an executable\nfpm test             # run tests", code),
         Paragraph("Language server workflow", h2),
         Paragraph("Install fortls from its official upstream instructions, configure your editor's Language Server Protocol client, and check the fortls repository for current configuration options. Project settings can live in a <font face='Courier'>.fortls</font> file in the workspace root. The FORTLS.com tools generate and check such files, but they verify syntax and known option names only, not full behavior.", p),
         Paragraph("Official references", h2),
         bl(["fortls: github.com/fortran-lang/fortls", "Fortran community: fortran-lang.org", "fpm: fpm.fortran-lang.org", "GNU Fortran: gcc.gnu.org/fortran"]),
         Spacer(1, 14),
         Paragraph("Free tools: fortls.com/tools. FORTLS.com is an independent resource hub and is not the official fortls project. Provided as-is without warranty.", small)]
    s += [PageBreak(), Paragraph("Arrays", h2),
         Preformatted("use iso_fortran_env, only: real64\nreal(real64), allocatable :: a(:)\nallocate(a(100))\na = 0.0_real64          ! whole-array assignment\na(2:5) = 1.0_real64     ! array section\nprint *, sum(a), size(a)", code),
         Paragraph("Modules and type-bound procedures", h2),
         Preformatted("module shapes\n  use iso_fortran_env, only: real64\n  implicit none\n  private\n  public :: circle\n\n  type :: circle\n    real(real64) :: r = 1.0_real64\n  contains\n    procedure :: area\n  end type circle\ncontains\n  pure function area(self) result(a)\n    class(circle), intent(in) :: self\n    real(real64) :: a\n    a = acos(-1.0_real64) * self%r**2\n  end function area\nend module shapes", code),
         Paragraph("Use <font face='Courier'>type, extends(parent)</font> for inheritance and <font face='Courier'>class(parent)</font> for polymorphic arguments.", p),
         Paragraph("VS Code workflow", h2),
         bl(["Install Python 3, then <font face='Courier'>pip install fortls</font>.", "Install the Modern Fortran extension (<font face='Courier'>fortran-lang.linter-gfortran</font>) and open your project folder.", "Add a <font face='Courier'>.fortls</font> file for <font face='Courier'>source_dirs</font> and <font face='Courier'>excl_paths</font> if the defaults do not fit.", "Install gfortran or ifx if you want compiler errors in the editor."]),
         Spacer(1, 10), Paragraph("Guides: fortls.com/blog - Tools: fortls.com/tools. Independent resource, not the official fortls project. Provided as-is without warranty.", small)]
    doc.build(s)
if __name__ == "__main__": build("quick-reference.pdf")
