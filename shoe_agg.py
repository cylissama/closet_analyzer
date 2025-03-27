import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from collections import Counter
import numpy as np
import sys
import os

def get_shoe_data():
    """Collects shoe data from user input."""
    shoes = []
    
    try:
        num_shoes = int(input("How many shoes do you have in your collection? "))
        
        for i in range(1, num_shoes + 1):
            print(f"\nShoe #{i}")
            brand = input("Brand: ").strip().capitalize()
            name = input("Name/Model: ").strip().capitalize()
            color = input("Color: ").strip().capitalize()
            while True:
                usage = input("Usage (Casual, Athletic, Formal): ").strip().capitalize()
                if usage in ["Casual", "Athletic", "Formal"]:
                    break
                else:
                    print("Invalid usage. Please choose from: Casual, Athletic, Formal.")
            
            size_input = input("Size (numerical): ").strip()
            try:
                size = float(size_input)
            except ValueError:
                print("Invalid size input. Using 0 as default.")
                size = 0
            
            shoes.append({
                'brand': brand,
                'name': name,
                'color': color,
                'usage': usage,
                'size': size
            })
        
        return shoes
    
    except ValueError:
        print("Please enter a valid number of shoes.")
        return get_shoe_data()

def read_shoe_data_from_file(filename):
    """Reads shoe data from a text file."""
    shoes = []
    
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            
            # Skip header line
            for line in lines[1:]:
                if line.strip() and not line.strip().startswith('#'):  # Skip empty lines and comments
                    parts = line.strip().split(',')
                    if len(parts) >= 5:  # Ensure we have all fields: brand, name, color, usage, size
                        brand = parts[0].strip().capitalize()
                        name = parts[1].strip().capitalize()
                        color = parts[2].strip().capitalize()
                        usage = parts[3].strip().capitalize()
                        
                        # Validate usage
                        if usage not in ["Casual", "Athletic", "Formal"]:
                            print(f"Warning: Invalid usage '{usage}' found in file. Defaulting to 'Casual'.")
                            usage = "Casual"
                        
                        try:
                            size = float(parts[4].strip())
                        except ValueError:
                            print(f"Warning: Invalid size '{parts[4].strip()}' found in file. Using 0 as default.")
                            size = 0
                        
                        shoes.append({
                            'brand': brand,
                            'name': name,
                            'color': color,
                            'usage': usage,
                            'size': size
                        })
            
            if not shoes:
                print("No valid data found in the file.")
                return None
            
            return shoes
    
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def create_template_file(filename="shoe_data_template.txt"):
    """Creates a template file for shoe data."""
    try:
        with open(filename, 'w') as file:
            file.write("Brand,Name,Color,Usage,Size\n")
            file.write("# Usage must be one of: Casual, Athletic, Formal\n")
            file.write("# Example entries below:\n")
            file.write("Nike,Air Max,Black,Athletic,10.5\n")
            file.write("Adidas,Superstar,White,Casual,11\n")
            file.write("Allen Edmonds,Park Avenue,Brown,Formal,10\n")
        
        print(f"Template file created: {filename}")
        print("Format: Brand,Name,Color,Usage,Size (one shoe per line)")
        print("Usage must be one of: Casual, Athletic, Formal")
    
    except Exception as e:
        print(f"An error occurred while creating the template file: {e}")

def create_dataframe(shoes):
    """Converts shoe data list to pandas DataFrame."""
    return pd.DataFrame(shoes)

def analyze_shoes(df, save_figures=False):
    """Analyzes shoe data and creates visualizations.
    
    Args:
        df: DataFrame containing shoe data
        save_figures: If True, figures will be saved without displaying them
    """
    if df.empty:
        print("No shoe data available for analysis.")
        return
    
    # Set up the plotting style - modern, clean look
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Color palette - use a professional color scheme
    colors = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47', '#F15C80', '#9B59B6', '#3498DB', '#2ECC71']
    pie_colors = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47', '#F15C80', '#9B59B6', '#3498DB', '#2ECC71', 
                 '#8E44AD', '#F39C12', '#D35400', '#C0392B', '#BDC3C7', '#1ABC9C']  # More colors for pie chart
    
    # Create a figure with subplots
    fig = plt.figure(figsize=(18, 14))
    fig.patch.set_facecolor('#F5F5F5')  # Light grey background
    
    # Add a stylish title
    fig.suptitle('Shoe Collection Analysis', fontsize=22, fontweight='bold', y=0.98, color='#303030')
    plt.figtext(0.5, 0.94, f'Total Shoes: {len(df)}', ha='center', fontsize=14, fontstyle='italic', color='#505050')
    
    # Create subplots with spacing
    gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.3)
    
    # 1. Color Distribution (Pie Chart)
    ax1 = fig.add_subplot(gs[0, 0])
    color_counts = df['color'].value_counts()
    wedges, texts, autotexts = ax1.pie(
        color_counts, 
        labels=None,  # No labels on the pie directly
        autopct='%1.1f%%', 
        startangle=90,
        colors=pie_colors,
        wedgeprops={'width': 0.6, 'edgecolor': 'w', 'linewidth': 2},  # Donut chart style
        textprops={'fontsize': 10, 'color': 'white', 'fontweight': 'bold'}
    )
    # Draw a white circle at the center to create a donut chart
    centre_circle = plt.Circle((0, 0), 0.3, fc='white')
    ax1.add_patch(centre_circle)
    
    # Add legend outside the pie
    ax1.legend(wedges, color_counts.index, title="Colors", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    ax1.set_title('Distribution of Shoe Colors', fontsize=14, fontweight='bold', pad=20, color='#303030')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    
    # 2. Usage Distribution (Bar Chart)
    ax2 = fig.add_subplot(gs[0, 1])
    usage_counts = df['usage'].value_counts()
    
    # Fixed version for modern seaborn - use hue parameter instead of directly passing palette
    bars = sns.barplot(x=usage_counts.index, y=usage_counts.values, hue=usage_counts.index, 
                      ax=ax2, palette=colors[:len(usage_counts)], legend=False)
    
    # Add value labels on top of bars
    for i, bar in enumerate(bars.containers[0]):
        bars.text(
            bar.get_x() + bar.get_width()/2.,
            bar.get_height() + 0.3,
            f'{int(usage_counts.values[i])}',
            ha="center", va="bottom", fontsize=11, fontweight='bold', color='#505050'
        )
    
    ax2.set_title('Shoes by Usage Type', fontsize=14, fontweight='bold', pad=20, color='#303030')
    ax2.set_xlabel('Usage', fontsize=12, color='#505050')
    ax2.set_ylabel('Count', fontsize=12, color='#505050')
    plt.setp(ax2.get_xticklabels(), rotation=0, ha='center')
    
    # Style the grid
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 3. Size Distribution (Histogram) - Fixed for modern seaborn
    ax3 = fig.add_subplot(gs[0, 2])
    sns.histplot(df, x='size', bins=10, kde=True, ax=ax3, color=colors[0], line_kws={'color': colors[1], 'linewidth': 2})
    
    ax3.set_title('Distribution of Shoe Sizes', fontsize=14, fontweight='bold', pad=20, color='#303030')
    ax3.set_xlabel('Size', fontsize=12, color='#505050')
    ax3.set_ylabel('Count', fontsize=12, color='#505050')
    
    # Style the grid
    ax3.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 4. Brand Distribution (Bar Chart)
    ax4 = fig.add_subplot(gs[1, 0])
    brand_counts = df['brand'].value_counts().head(8)  # Top 8 brands
    
    # Fixed version for modern seaborn
    bars = sns.barplot(x=brand_counts.index, y=brand_counts.values, hue=brand_counts.index,
                      ax=ax4, palette=colors[:len(brand_counts)], legend=False)
    
    # Add value labels on top of bars
    for i, bar in enumerate(bars.containers[0]):
        bars.text(
            bar.get_x() + bar.get_width()/2.,
            bar.get_height() + 0.3,
            f'{int(brand_counts.values[i])}',
            ha="center", va="bottom", fontsize=11, fontweight='bold', color='#505050'
        )
    
    ax4.set_title('Top Brands in Collection', fontsize=14, fontweight='bold', pad=20, color='#303030')
    ax4.set_xlabel('Brand', fontsize=12, color='#505050')
    ax4.set_ylabel('Count', fontsize=12, color='#505050')
    plt.setp(ax4.get_xticklabels(), rotation=45, ha='right')
    
    # Style the grid
    ax4.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 5. Brand vs Usage (Stacked Bar Chart)
    ax5 = fig.add_subplot(gs[1, 1])
    # Create a crosstab for brand vs usage
    brand_usage = pd.crosstab(df['brand'], df['usage'])
    brand_usage = brand_usage.loc[brand_usage.sum(axis=1).sort_values(ascending=False).head(8).index]  # Top 8 brands
    brand_usage.plot(
        kind='bar', 
        stacked=True, 
        ax=ax5, 
        colormap='tab10',
        width=0.8
    )
    ax5.set_title('Brand by Usage Type', fontsize=14, fontweight='bold', pad=20, color='#303030')
    ax5.set_xlabel('Brand', fontsize=12, color='#505050')
    ax5.set_ylabel('Count', fontsize=12, color='#505050')
    plt.setp(ax5.get_xticklabels(), rotation=45, ha='right')
    
    # Style the grid
    ax5.grid(axis='y', linestyle='--', alpha=0.7)
    # Improve legend
    ax5.legend(title='Usage Type', frameon=True, edgecolor='#D3D3D3')
    
    # 6. Color vs Size boxplot
    ax6 = fig.add_subplot(gs[1, 2])
    sns.boxplot(
        x='color', 
        y='size', 
        data=df, 
        hue='color',  # Fixed for modern seaborn
        ax=ax6, 
        palette=pie_colors[:len(df['color'].unique())],
        width=0.6,
        flierprops={'marker': 'o', 'markerfacecolor': 'red', 'markersize': 6},
        legend=False  # Hide the legend since it's redundant with x-axis
    )
    ax6.set_title('Shoe Sizes by Color', fontsize=14, fontweight='bold', pad=20, color='#303030')
    ax6.set_xlabel('Color', fontsize=12, color='#505050')
    ax6.set_ylabel('Size', fontsize=12, color='#505050')
    plt.setp(ax6.get_xticklabels(), rotation=45, ha='right')
    
    # Style the grid
    ax6.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add a watermark signature
    fig.text(0.99, 0.01, 'Shoe Collection Analyzer', 
             ha='right', va='bottom', alpha=0.1, fontsize=20, fontweight='bold')
    
    # Adjust layout for the plots
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    
    # Create a styled table in a separate figure
    table_fig = plt.figure(figsize=(18, 8))
    table_fig.patch.set_facecolor('#F5F5F5')  # Light grey background
    
    # Add a stylish title
    table_fig.suptitle('Shoe Collection Inventory', fontsize=22, fontweight='bold', color='#303030')
    plt.figtext(0.5, 0.95, f'Total Shoes: {len(df)}', ha='center', fontsize=14, fontstyle='italic', color='#505050')
    
    # Format the table
    table_ax = plt.subplot(1, 1, 1)
    table_ax.axis('off')  # Hide the axes
    
    # Create a styled table
    cell_text = []
    for _, row in df.iterrows():
        cell_text.append([row['brand'], row['name'], row['color'], row['usage'], str(row['size'])])
        
    column_labels = ['Brand', 'Name', 'Color', 'Usage', 'Size']
    
    # Calculate optimal column widths
    col_widths = [0.2, 0.25, 0.2, 0.15, 0.1]
    
    # Create the table with a more modern look
    table = plt.table(
        cellText=cell_text,
        colLabels=column_labels,
        colWidths=col_widths,
        loc='center',
        cellLoc='center',
        bbox=[0.05, 0.05, 0.9, 0.85]  # Position the table properly
    )
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)  # Adjust row height
    
    # Style the header and rows with a modern color scheme
    header_color = '#4472C4'  # Blue header
    odd_row_color = '#EDF2F9'  # Very light blue for odd rows
    even_row_color = '#FFFFFF'  # White for even rows
    border_color = '#FFFFFF'  # White borders
    
    for (row, col), cell in table.get_celld().items():
        # Set cell edge color
        cell.set_edgecolor(border_color)
        
        if row == 0:  # Header row
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor(header_color)
        else:  # Alternate row colors for better readability
            if row % 2:
                cell.set_facecolor(odd_row_color)
            else:
                cell.set_facecolor(even_row_color)
    
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    
    # Show both figures (unless we're just saving)
    if not save_figures:
        plt.show()
    return fig, table_fig  # Return the figures for saving

def main():
    print("=== Shoe Collection Analyzer ===")
    
    # Check if the program is receiving piped input
    if not sys.stdin.isatty():
        print("Detecting piped input...")
        # Create a temporary file for the piped input
        temp_filename = "temp_shoe_data.txt"
        with open(temp_filename, 'w') as temp_file:
            temp_file.write(sys.stdin.read())
        
        print(f"Reading shoe data from piped input...")
        shoes = read_shoe_data_from_file(temp_filename)
        
        # Clean up the temporary file
        try:
            os.remove(temp_filename)
        except:
            pass
            
        if shoes is None or len(shoes) == 0:
            print("No valid data found in the piped input. Exiting program.")
            return
    else:
        print("This program will collect data about your shoes and display visualizations.")
        
        print("\nHow would you like to enter your shoe data?")
        print("1. Input data manually")
        print("2. Read data from a text file")
        print("3. Create a template file for future use")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            shoes = get_shoe_data()
        elif choice == '2':
            filename = input("Enter the path to your shoe data file: ").strip()
            shoes = read_shoe_data_from_file(filename)
            if shoes is None:
                print("Would you like to enter data manually instead? (y/n): ")
                if input().lower() == 'y':
                    shoes = get_shoe_data()
                else:
                    print("Exiting program.")
                    return
        elif choice == '3':
            filename = input("Enter filename for template (default: shoe_data_template.txt): ").strip()
            if not filename:
                filename = "shoe_data_template.txt"
            create_template_file(filename)
            print("Would you like to enter data manually now? (y/n): ")
            if input().lower() == 'y':
                shoes = get_shoe_data()
            else:
                print("Exiting program.")
                return
        else:
            print("Invalid choice. Exiting program.")
            return
    
    df = create_dataframe(shoes)
    
    # Check if we're in piped mode
    is_piped_input = not sys.stdin.isatty()
    
    print("\nAnalyzing your shoe collection...")
    charts_fig, table_fig = analyze_shoes(df, save_figures=is_piped_input)
    
    # Check if we're in piped mode to avoid EOF error
    is_piped_input = not sys.stdin.isatty()
    
    if is_piped_input:
        # When using piped input, automatically save files without prompting
        # Save CSV data
        csv_filename = "shoe_collection.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Data saved to {csv_filename}")
        
        # Save figures automatically
        print("Saving visualization figures...")
        # Save the figures using the references we have
        charts_fig.savefig("shoe_collection_charts.png", dpi=300, bbox_inches='tight')
        print("Charts saved to 'shoe_collection_charts.png'")
        
        table_fig.savefig("shoe_collection_table.png", dpi=300, bbox_inches='tight')
        print("Table saved to 'shoe_collection_table.png'")
        
        print("Figure display complete.")
    else:
        # Interactive mode - ask the user
        try:
            # Save data to CSV (optional)
            save_option = input("\nWould you like to save your shoe data to a CSV file? (y/n): ").lower()
            if save_option == 'y':
                filename = input("Enter filename (default: shoe_collection.csv): ").strip()
                if not filename:
                    filename = "shoe_collection.csv"
                if not filename.endswith('.csv'):
                    filename += '.csv'
                df.to_csv(filename, index=False)
                print(f"Data saved to {filename}")
            
            # Save figures (optional)
            save_figs = input("\nWould you like to save the visualization figures? (y/n): ").lower()
            if save_figs == 'y':
                charts_filename = input("Enter filename for charts (default: shoe_collection_charts.png): ").strip()
                if not charts_filename:
                    charts_filename = "shoe_collection_charts.png"
                if not charts_filename.lower().endswith(('.png', '.jpg', '.pdf', '.svg')):
                    charts_filename += '.png'
                
                # Save charts using the figure reference
                charts_fig.savefig(charts_filename, dpi=300, bbox_inches='tight')
                print(f"Charts saved to '{charts_filename}'")
                
                table_filename = input("Enter filename for table (default: shoe_collection_table.png): ").strip()
                if not table_filename:
                    table_filename = "shoe_collection_table.png"
                if not table_filename.lower().endswith(('.png', '.jpg', '.pdf', '.svg')):
                    table_filename += '.png'
                
                # Save table using the figure reference
                table_fig.savefig(table_filename, dpi=300, bbox_inches='tight')
                print(f"Table saved to '{table_filename}'")
        except EOFError:
            # Handle any unexpected EOF errors
            print("\nInput error detected. Saving data with default filenames.")
            df.to_csv("shoe_collection.csv", index=False)
            print("Data saved to 'shoe_collection.csv'")
            
            charts_fig.savefig("shoe_collection_charts.png", dpi=300, bbox_inches='tight')
            table_fig.savefig("shoe_collection_table.png", dpi=300, bbox_inches='tight')
            print("Figures saved with default filenames.")
    
    print("Thank you for using the Shoe Collection Analyzer!")

if __name__ == "__main__":
    main()