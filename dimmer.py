import tkinter as tk
from tkinter import ttk, Scale
import sys

# Проверка доступности библиотек для управления фонариком
try:
    if sys.platform == 'win32':
        # Для Windows можно использовать библиотеку like pygetwindow или другие
        # Здесь используем заглушку, так как прямой доступ к фонарику на Windows сложен
        has_flashlight = False
        print("На Windows управление фонариком может потребовать дополнительных библиотек")
    else:
        # Для Android/Linux (например, через Kivy или другие фреймворки)
        has_flashlight = False
except:
    has_flashlight = False

class LEDDimmerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LED Dimmer Control")
        self.root.geometry("400x500")
        
        # Переменные состояния
        self.led_on = False
        self.brightness = 50  # начальная яркость 50%
        
        # Стилизация
        self.setup_styles()
        
        # Создание интерфейса
        self.create_widgets()
        
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.theme_use('clam')
        
    def create_widgets(self):
        """Создание элементов интерфейса"""
        
        # Заголовок
        title_label = ttk.Label(
            self.root, 
            text="ДИММЕР ДЛЯ ФОНАРИКА", 
            font=('Arial', 18, 'bold')
        )
        title_label.pack(pady=20)
        
        # Индикатор состояния
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(pady=10)
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="СТАТУС: ВЫКЛ",
            font=('Arial', 14),
            foreground='red'
        )
        self.status_label.pack()
        
        # Кнопка включения/выключения
        self.toggle_button = ttk.Button(
            self.root,
            text="ВКЛЮЧИТЬ",
            command=self.toggle_led,
            width=20
        )
        self.toggle_button.pack(pady=20)
        
        # Слайдер для регулировки яркости
        brightness_frame = ttk.LabelFrame(self.root, text="Регулировка яркости", padding=10)
        brightness_frame.pack(pady=20, padx=20, fill='x')
        
        ttk.Label(brightness_frame, text="Яркость:").pack(anchor='w')
        
        self.brightness_scale = ttk.Scale(
            brightness_frame,
            from_=0,
            to=100,
            orient='horizontal',
            command=self.update_brightness,
            length=300
        )
        self.brightness_scale.set(self.brightness)
        self.brightness_scale.pack(pady=10, fill='x')
        
        # Отображение значения яркости
        self.brightness_value = ttk.Label(
            brightness_frame,
            text=f"{self.brightness}%",
            font=('Arial', 12)
        )
        self.brightness_value.pack()
        
        # Индикатор яркости (визуализация)
        self.brightness_canvas = tk.Canvas(
            self.root,
            width=300,
            height=30,
            bg='white',
            highlightthickness=1,
            highlightbackground='gray'
        )
        self.brightness_canvas.pack(pady=10)
        self.update_brightness_display()
        
        # Информационная панель
        info_frame = ttk.Frame(self.root)
        info_frame.pack(pady=20, fill='x', padx=20)
        
        ttk.Label(
            info_frame,
            text="Управление фонариком устройства",
            font=('Arial', 10)
        ).pack()
        
        if not has_flashlight:
            ttk.Label(
                info_frame,
                text="Для реального управления фонариком установите библиотеку:\n"
                     "Windows: pygetwindow + дополнительные инструменты\n"
                     "Android: python-for-android с доступом к камере",
                foreground='orange',
                font=('Arial', 8),
                justify='center'
            ).pack(pady=5)
        
        # Кнопка выхода
        ttk.Button(
            self.root,
            text="ВЫХОД",
            command=self.root.quit,
            width=15
        ).pack(pady=10)
        
    def toggle_led(self):
        """Включение/выключение светодиода"""
        self.led_on = not self.led_on
        
        if self.led_on:
            self.status_label.config(text="СТАТУС: ВКЛ", foreground='green')
            self.toggle_button.config(text="ВЫКЛЮЧИТЬ")
            self.turn_on_led()
        else:
            self.status_label.config(text="СТАТУС: ВЫКЛ", foreground='red')
            self.toggle_button.config(text="ВКЛЮЧИТЬ")
            self.turn_off_led()
        
        self.update_brightness_display()
    
    def turn_on_led(self):
        """Включение фонарика с текущей яркостью"""
        brightness_value = self.brightness
        
        if has_flashlight:
            # Здесь будет код для реального управления фонариком
            pass
        else:
            print(f"ФОНАРИК ВКЛ (эмуляция) - Яркость: {brightness_value}%")
        
        self.update_brightness_display()
    
    def turn_off_led(self):
        """Выключение фонарика"""
        if has_flashlight:
            # Здесь будет код для выключения фонарика
            pass
        else:
            print("ФОНАРИК ВЫКЛ (эмуляция)")
    
    def update_brightness(self, value):
        """Обновление значения яркости"""
        try:
            self.brightness = int(float(value))
            self.brightness_value.config(text=f"{self.brightness}%")
            
            if self.led_on:
                self.turn_on_led()
            
            self.update_brightness_display()
        except ValueError:
            pass
    
    def update_brightness_display(self):
        """Обновление визуального отображения яркости"""
        self.brightness_canvas.delete("all")
        
        width = 300
        height = 30
        
        # Фон
        self.brightness_canvas.create_rectangle(
            0, 0, width, height,
            fill='light gray',
            outline=''
        )
        
        if self.led_on:
            # Индикатор яркости
            led_width = int(width * self.brightness / 100)
            
            # Градиент от желтого к оранжевому
            for i in range(led_width):
                # Вычисление цвета от светлого к темному
                intensity = int(255 - (i / led_width) * 100)
                if intensity < 155:
                    intensity = 155
                
                color = f'#{intensity:02x}{int(intensity*0.8):02x}00'
                
                self.brightness_canvas.create_rectangle(
                    i, 0, i+1, height,
                    fill=color,
                    outline=''
                )
            
            # Обводка
            self.brightness_canvas.create_rectangle(
                0, 0, led_width, height,
                outline='dark orange',
                width=1
            )
            
            # Текст яркости на индикаторе
            self.brightness_canvas.create_text(
                led_width//2, height//2,
                text=f"{self.brightness}%",
                fill='black' if self.brightness > 50 else 'white',
                font=('Arial', 10, 'bold')
            )
        else:
            # Серый индикатор при выключенном состоянии
            self.brightness_canvas.create_text(
                width//2, height//2,
                text="ВЫКЛ",
                fill='gray',
                font=('Arial', 10, 'bold')
            )

def main():
    root = tk.Tk()
    app = LEDDimmerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
