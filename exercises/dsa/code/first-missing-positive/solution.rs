impl Solution {
    pub fn first_missing_positive(mut nums: Vec<i32>) -> i32 {
        let n = nums.len();
        // Use the vector itself as the table: number v belongs at position v - 1.
        for i in 0..n {
            // Keep swapping until this slot holds something that can't be placed,
            // or already sits where it belongs.
            while nums[i] >= 1 && (nums[i] as usize) <= n && nums[nums[i] as usize - 1] != nums[i] {
                let home = nums[i] as usize - 1;
                nums.swap(i, home);
            }
        }
        // The first slot not holding its own number marks the gap.
        for i in 0..n {
            if nums[i] != i as i32 + 1 {
                return i as i32 + 1;
            }
        }
        n as i32 + 1
    }
}
