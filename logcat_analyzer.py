import subprocess
import re
from collections import Counter
from datetime import datetime

class LogcatAnalyzer:
    def __init__(self):
        self.log_levels = {
            'V': 'Verbose',
            'D': 'Debug',
            'I': 'Info',
            'W': 'Warning',
            'E': 'Error',
            'F': 'Fatal'
        }
    
    def capture_logcat(self, duration=10, output_file='logcat.txt'):
        """Capture logcat for specified duration in seconds"""
        print(f"Capturing logcat for {duration} seconds...")
        try:
            # Clear old logs first
            subprocess.run(['adb', 'logcat', '-c'], check=False)
            
            # Capture logcat
            with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
                process = subprocess.Popen(
                    ['adb', 'logcat', '-v', 'time'],
                    stdout=f,
                    stderr=subprocess.PIPE
                )
                process.wait(timeout=duration)
        except subprocess.TimeoutExpired:
            process.kill()
            print(f"Logcat captured and saved to {output_file}")
        except Exception as e:
            print(f"Error capturing logcat: {e}")
            return False
        return True
    
    def parse_logcat_line(self, line):
        """Parse a logcat line and extract components"""
        # Skip separator lines
        if line.startswith('--------- beginning of'):
            return None
        
        # Pattern: MM-DD HH:MM:SS.mmm LEVEL/TAG(PID): Message
        # Example: 12-31 14:19:40.332 D/BatteryChargeControl( 2026): message
        pattern = r'(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+)\s+([VDIWEF])/([^(]+)\(\s*(\d+)\):\s*(.*)'
        match = re.match(pattern, line.strip())
        if match:
            return {
                'timestamp': match.group(1),
                'level': match.group(2),
                'tag': match.group(3).strip(),
                'pid': match.group(4),
                'message': match.group(5)
            }
        return None
    
    def analyze_file(self, filename='logcat.txt'):
        """Analyze the logcat file and provide statistics"""
        print(f"\n{'='*60}")
        print(f"LOGCAT ANALYSIS: {filename}")
        print(f"{'='*60}\n")
        
        level_counter = Counter()
        tag_counter = Counter()
        errors = []
        warnings = []
        
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    parsed = self.parse_logcat_line(line)
                    if parsed:
                        level_counter[parsed['level']] += 1
                        tag_counter[parsed['tag']] += 1
                        
                        if parsed['level'] == 'E':
                            errors.append(f"{parsed['tag']}: {parsed['message'][:100]}")
                        elif parsed['level'] == 'W':
                            warnings.append(f"{parsed['tag']}: {parsed['message'][:100]}")
        except FileNotFoundError:
            print(f"File {filename} not found!")
            return
        
        # Display statistics
        print("📊 LOG LEVEL DISTRIBUTION:")
        total_logs = sum(level_counter.values())
        for level in ['E', 'W', 'I', 'D', 'V', 'F']:
            count = level_counter[level]
            if count > 0:
                percentage = (count / total_logs) * 100
                print(f"  {level} ({self.log_levels[level]:8s}): {count:6d} ({percentage:5.2f}%)")
        
        print(f"\n📝 TOTAL LOG ENTRIES: {total_logs}")
        
        print(f"\n🏷️  TOP 10 MOST ACTIVE TAGS:")
        for tag, count in tag_counter.most_common(10):
            print(f"  {count:6d} - {tag}")
        
        if errors:
            print(f"\n❌ ERRORS FOUND ({len(errors)} total):")
            for i, error in enumerate(errors[:10], 1):
                print(f"  {i}. {error}")
            if len(errors) > 10:
                print(f"  ... and {len(errors) - 10} more errors")
        
        if warnings:
            print(f"\n⚠️  WARNINGS FOUND ({len(warnings)} total):")
            for i, warning in enumerate(warnings[:10], 1):
                print(f"  {i}. {warning}")
            if len(warnings) > 10:
                print(f"  ... and {len(warnings) - 10} more warnings")
        
        print(f"\n{'='*60}\n")
    
    def filter_by_level(self, input_file='logcat.txt', level='E', output_file=None):
        """Filter logcat by log level"""
        if output_file is None:
            output_file = f'logcat_{level.lower()}.txt'
        
        count = 0
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f_in:
            with open(output_file, 'w', encoding='utf-8') as f_out:
                for line in f_in:
                    parsed = self.parse_logcat_line(line)
                    if parsed and parsed['level'] == level:
                        f_out.write(line)
                        count += 1
        
        print(f"Filtered {count} {self.log_levels[level]} entries to {output_file}")
        return output_file
    
    def filter_by_tag(self, input_file='logcat.txt', tag='', output_file=None):
        """Filter logcat by tag"""
        if output_file is None:
            output_file = f'logcat_{tag.replace(" ", "_")}.txt'
        
        count = 0
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f_in:
            with open(output_file, 'w', encoding='utf-8') as f_out:
                for line in f_in:
                    parsed = self.parse_logcat_line(line)
                    if parsed and tag.lower() in parsed['tag'].lower():
                        f_out.write(line)
                        count += 1
        
        print(f"Filtered {count} entries with tag '{tag}' to {output_file}")
        return output_file
    
    def search_keyword(self, input_file='logcat.txt', keyword='', case_sensitive=False):
        """Search for keyword in logcat"""
        print(f"\n🔍 Searching for '{keyword}'...\n")
        count = 0
        
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                if case_sensitive:
                    if keyword in line:
                        print(f"Line {line_num}: {line.strip()}")
                        count += 1
                else:
                    if keyword.lower() in line.lower():
                        print(f"Line {line_num}: {line.strip()}")
                        count += 1
                
                if count >= 20:  # Limit to 20 results
                    print(f"\n... showing first 20 results (found more)")
                    break
        
        if count == 0:
            print(f"No matches found for '{keyword}'")
        else:
            print(f"\nTotal matches: {count}")
    
    def create_critical_report(self, input_file='logcat.txt', output_file='critical_report.txt'):
        """Create a clean report focusing on critical issues"""
        print(f"\n📋 Generating critical issues report...\n")
        
        errors = []
        warnings = []
        error_tags = Counter()
        warning_tags = Counter()
        unique_errors = Counter()
        unique_warnings = Counter()
        
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                parsed = self.parse_logcat_line(line)
                if parsed:
                    if parsed['level'] == 'E':
                        errors.append(parsed)
                        error_tags[parsed['tag']] += 1
                        # Group similar errors
                        error_key = f"{parsed['tag']}: {parsed['message'][:50]}"
                        unique_errors[error_key] += 1
                    elif parsed['level'] == 'W':
                        warnings.append(parsed)
                        warning_tags[parsed['tag']] += 1
                        warning_key = f"{parsed['tag']}: {parsed['message'][:50]}"
                        unique_warnings[warning_key] += 1
        
        # Generate report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("ANDROID LOGCAT - CRITICAL ISSUES REPORT\n")
            f.write("="*80 + "\n\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Source File: {input_file}\n")
            f.write(f"Total Errors: {len(errors)}\n")
            f.write(f"Total Warnings: {len(warnings)}\n")
            f.write("\n" + "="*80 + "\n\n")
            
            # Priority 1: Most frequent errors
            f.write("🚨 PRIORITY 1: MOST FREQUENT ERRORS\n")
            f.write("-"*80 + "\n")
            for error, count in unique_errors.most_common(10):
                f.write(f"  [{count}x] {error}\n")
            f.write("\n")
            
            # Priority 2: Components with most errors
            f.write("⚠️  PRIORITY 2: COMPONENTS WITH MOST ERRORS\n")
            f.write("-"*80 + "\n")
            for tag, count in error_tags.most_common(10):
                f.write(f"  {count:3d} errors - {tag}\n")
            f.write("\n")
            
            # Priority 3: Unique error messages
            f.write("📝 PRIORITY 3: UNIQUE ERROR MESSAGES (First 20)\n")
            f.write("-"*80 + "\n")
            seen_messages = set()
            error_count = 0
            for error in errors:
                message_key = f"{error['tag']}: {error['message'][:80]}"
                if message_key not in seen_messages and error_count < 20:
                    seen_messages.add(message_key)
                    f.write(f"\n[{error['timestamp']}] {error['tag']}\n")
                    f.write(f"  {error['message']}\n")
                    error_count += 1
            f.write("\n")
            
            # Warning summary
            f.write("⚡ WARNING SUMMARY\n")
            f.write("-"*80 + "\n")
            for tag, count in warning_tags.most_common(10):
                f.write(f"  {count:3d} warnings - {tag}\n")
            f.write("\n")
            
            # Recommendations
            f.write("💡 RECOMMENDATIONS\n")
            f.write("-"*80 + "\n")
            f.write("1. Focus on components with repeated errors\n")
            f.write("2. Check network connectivity (DNS resolution failures)\n")
            f.write("3. Verify app permissions for socket operations\n")
            f.write("4. Review system resource configurations\n")
            f.write("\n" + "="*80 + "\n")
        
        print(f"✅ Critical issues report saved to: {output_file}")
        print(f"   Total Errors: {len(errors)}")
        print(f"   Total Warnings: {len(warnings)}")
        print(f"   Unique Error Types: {len(unique_errors)}")
        return output_file
    
    def monitor_app(self, package_or_tag='', duration=30, output_file=None):
        """Monitor specific app or component in real-time"""
        if not output_file:
            safe_name = package_or_tag.replace('.', '_').replace(' ', '_')
            output_file = f'monitor_{safe_name}.txt'
        
        print(f"\n🔍 Monitoring '{package_or_tag}' for {duration} seconds...")
        print("Press Ctrl+C to stop early\n")
        
        try:
            # Clear logcat
            subprocess.run(['adb', 'logcat', '-c'], check=False)
            
            # Start monitoring with filter
            with open(output_file, 'w', encoding='utf-8', errors='ignore') as f:
                # Use grep/findstr to filter
                if package_or_tag:
                    process = subprocess.Popen(
                        ['adb', 'logcat', '-v', 'time'],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        encoding='utf-8',
                        errors='ignore'
                    )
                    
                    start_time = datetime.now()
                    line_count = 0
                    error_count = 0
                    warning_count = 0
                    
                    while (datetime.now() - start_time).seconds < duration:
                        line = process.stdout.readline()
                        if not line:
                            break
                        
                        # Filter for package/tag
                        if package_or_tag.lower() in line.lower():
                            f.write(line)
                            line_count += 1
                            
                            # Count errors and warnings
                            if ' E/' in line:
                                error_count += 1
                                print(f"❌ {line.strip()}")
                            elif ' W/' in line:
                                warning_count += 1
                                print(f"⚠️  {line.strip()}")
                            elif ' I/' in line or ' D/' in line:
                                print(f"ℹ️  {line.strip()}")
                    
                    process.kill()
                    
                    print(f"\n{'='*60}")
                    print(f"Monitoring complete!")
                    print(f"  Total lines captured: {line_count}")
                    print(f"  Errors: {error_count}")
                    print(f"  Warnings: {warning_count}")
                    print(f"  Saved to: {output_file}")
                    print(f"{'='*60}\n")
                    
        except KeyboardInterrupt:
            print(f"\n\n⏹️  Monitoring stopped by user.")
            print(f"   Logs saved to: {output_file}")
        except Exception as e:
            print(f"Error during monitoring: {e}")
        
        return output_file


def main():
    analyzer = LogcatAnalyzer()
    
    print("Android Logcat Analyzer")
    print("=" * 60)
    print("\nOptions:")
    print("1. Capture new logcat (10 seconds)")
    print("2. Capture new logcat (30 seconds)")
    print("3. Analyze existing logcat.txt")
    print("4. Filter by error level (E)")
    print("5. Filter by warning level (W)")
    print("6. Filter by tag")
    print("7. Search for keyword")
    print("8. Get live logcat stream (Ctrl+C to stop)")
    print("9. 📋 Generate critical issues report")
    print("10. 🔍 Monitor specific app/component")
    
    choice = input("\nEnter your choice (1-10): ").strip()
    
    if choice == '1':
        analyzer.capture_logcat(duration=10)
        analyzer.analyze_file()
    
    elif choice == '2':
        analyzer.capture_logcat(duration=30)
        analyzer.analyze_file()
    
    elif choice == '3':
        analyzer.analyze_file()
    
    elif choice == '4':
        analyzer.filter_by_level(level='E')
    
    elif choice == '5':
        analyzer.filter_by_level(level='W')
    
    elif choice == '6':
        tag = input("Enter tag to filter: ").strip()
        analyzer.filter_by_tag(tag=tag)
    
    elif choice == '7':
        keyword = input("Enter keyword to search: ").strip()
        analyzer.search_keyword(keyword=keyword)
    
    elif choice == '8':
        print("Starting live logcat stream (press Ctrl+C to stop)...")
        try:
            subprocess.run(['adb', 'logcat', '-v', 'time'])
        except KeyboardInterrupt:
            print("\n\nLogcat stream stopped.")
    
    elif choice == '9':
        # Check if logcat.txt exists
        import os
        if os.path.exists('logcat.txt'):
            analyzer.create_critical_report()
            print("\n💡 Tip: Open 'critical_report.txt' to view the detailed analysis")
        else:
            print("❌ No logcat.txt found. Please capture logs first (option 1 or 2).")
    
    elif choice == '10':
        package = input("Enter app package name (e.g., 'com.facebook.messenger') or component tag to monitor: ").strip()
        if package:
            duration_input = input("Monitor duration in seconds (default 30): ").strip()
            duration = int(duration_input) if duration_input.isdigit() else 30
            analyzer.monitor_app(package, duration)
            print("\n💡 Tip: You can analyze the captured file using option 3")
        else:
            print("❌ Package/tag name is required.")
    
    else:
        print("Invalid choice!")


if __name__ == '__main__':
    main()
