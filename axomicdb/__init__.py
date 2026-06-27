cat > axomicdb/__init__.py << 'EOF'
from .database import Database
from .table import Table

__all__ = ['Database', 'Table']
EOF
