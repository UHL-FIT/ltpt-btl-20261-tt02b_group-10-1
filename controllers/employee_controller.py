from models.employee import Employee 
from utils.file_handler import load_json, save_json 
# Định nghĩa lớp EmployeeController, đóng vai trò quản lý các thao tác với dữ liệu nhân viên
class EmployeeController:
    # Hàm khởi tạo, nhận vào một hàm callback 'on_changed' (mặc định là None nếu không truyền)
    def __init__(self, on_changed=None): 

        # Lưu trữ hàm callback này vào thuộc tính private. Hàm này thường dùng để reload UI khi dữ liệu đổi.
        self._on_changed = on_changed 

        # Hàm private dùng để phát thông báo mỗi khi dữ liệu bị thay đổi (thêm, xóa...)
    def _notify(self): 
        # Kiểm tra xem lúc khởi tạo có truyền hàm callback vào không
        if self._on_changed: 
            self._on_changed() # Nếu có, gọi hàm đó thực thi

    # Hàm lấy danh sách tất cả nhân viên (luôn được sắp xếp theo ID)
    def list_employees(self): 
        """Lấy danh sách đối tượng Employee từ file json."""
        raw = load_json("employees.json", default=[]) # Đọc dữ liệu từ file "employees.json". Nếu file lỗi/trống, trả về list rỗng []
        out = [] #tạo 1 ds rỗng
        for item in raw: 
            try: 
                out.append(Employee.from_dict(item)) # Chuyển đổi dict thành object Employee và thêm vào danh sách 'out'
            except Exception: 
                continue 
        # Sắp xếp theo ID số nguyên tăng dần từ 1 trở đi
        try:
            out.sort(key=lambda e: int(e.id))
        except Exception:
            pass
        return out # Trả về danh sách các đối tượng Employee hợp lệ

    def add_employee(self, full_name, department, base_salary, allowance, deduction): # Hàm tạo và thêm nhân viên mới
        """Thêm một nhân viên mới."""
        # Lấy danh sách nhân viên để xử lý
        employees = self.list_employees() 
        
        # Tự động sinh ID tiếp theo (Tìm ID số nguyên nhỏ nhất còn trống bắt đầu từ 1)
        used_ids = set()
        for e in employees:
            try:
                used_ids.add(int(e.id))
            except ValueError:
                pass
        
        next_id = 1
        while next_id in used_ids:
            next_id += 1 
        # Khởi tạo một đối tượng nhân viên mới với các thông số truyền vào
        emp = Employee( 
            id=str(next_id), # Gán ID mới vừa tính toán được (chuyển ngược lại thành chuỗi string)
            full_name=full_name.strip(), # Gán tên và cắt bỏ khoảng trắng thừa ở hai đầu bằng strip()
            department=department.strip(), # Gán tên phòng ban và cắt bỏ khoảng trắng thừa
            base_salary=base_salary, # Gán mức lương cơ bản
            allowance=allowance, # Gán mức phụ cấp
            deduction=deduction # Gán mức khấu trừ
        )
        employees.append(emp) # Thêm object nhân viên mới vào danh sách hiện tại
        # Sắp xếp lại danh sách theo ID tăng dần trước khi lưu vào JSON
        try:
            employees.sort(key=lambda e: int(e.id))
        except Exception:
            pass
        save_json("employees.json", [e.to_dict() for e in employees]) # Chuyển tất cả object thành dict và lưu đè lại vào file JSON
        self._notify() # Báo hiệu dữ liệu đã thay đổi (để cập nhật giao diện nếu cần)
        return emp # Trả về đối tượng nhân viên vừa được tạo

    def update_employee(self, emp_id, full_name, department, base_salary, allowance, deduction):
        """Cập nhật thông tin nhân viên."""
        employees = self.list_employees()
        updated = False
        for e in employees:
            if e.id == emp_id:
                e.full_name = full_name.strip()
                e.department = department.strip()
                e.base_salary = base_salary
                e.allowance = allowance
                e.deduction = deduction
                updated = True
                break
        if updated:
            save_json("employees.json", [e.to_dict() for e in employees])
            self._notify()
            return True
        return False
    
    # Hàm xóa nhân viên dựa vào ID
    def delete_employee(self, emp_id):
        """Xóa nhân viên theo ID."""
        employees = self.list_employees() # Lấy danh sách nhân viên hiện tại
        initial_len = len(employees) # Lưu lại số lượng nhân viên ban đầu
        # Dùng List Comprehension tạo danh sách mới, chỉ giữ lại những ai có ID KHÁC với ID cần xóa
        employees = [e for e in employees if e.id != emp_id] 

        # Kiểm tra xem độ dài danh sách mới có ngắn hơn ban đầu không (tức là đã tìm thấy và xóa)
        if len(employees) < initial_len: 
            save_json("employees.json", [e.to_dict() for e in employees]) # Lưu danh sách mới vào file JSON
            self._notify() 
            return True 
        return False
    
    # (Đã xóa hàm thống kê giờ làm thêm)

    def get_salary_growth_rate(self): #hàm
        """Tính tỷ lệ tăng trưởng lương trung bình."""
        employees = self.list_employees() # Lấy danh sách nhân viên
        if not employees: 
            return 0.0
        # Tính lương trung bình: Cộng dồn lương thực nhận (net_salary) của mọi người rồi chia cho tổng số người
        avg_net_salary = sum(e.net_salary() for e in employees) / len(employees)
        
        # Giả lập: Lương kỳ trước bằng 95% lương kỳ này (Do hệ thống không lưu lịch sử lương cũ)
        avg_net_salary_prev = avg_net_salary * 0.95 
        
        if avg_net_salary_prev == 0: # Đề phòng trường hợp chia cho 0 nếu lương kỳ trước là 0
            return 0.0
            
        # Công thức tính tỷ lệ tăng trưởng: ((Mới - Cũ) / Cũ) * 100
        rate = ((avg_net_salary - avg_net_salary_prev) / avg_net_salary_prev) * 100 
        return round(rate, 2) # Làm tròn kết quả đến 2 chữ số thập phân rồi trả về
