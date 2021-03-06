import gym

from envs.common_wrappers import NoopResetEnv, ClipRewardEnv, MaxAndSkipEnv, ProcessFrame84
from envs.common_wrappers import FrameStack, ExtraTimeLimit, ImageToPyTorch, NormalizedEnv
from envs.dm_lab_env import Dmlab_env

def make_atari(args):
    args = args.environment
    env = gym.make(args.env_name)
    env = NoopResetEnv(env, noop_max=args.noop_max)
    if args.clip_rewards:
        env = ClipRewardEnv(env)
    if 'NoFrameskip' in env.spec.id and args.skip_frames > 0:
        env = MaxAndSkipEnv(env, skip=args.skip_frames)
    env = ProcessFrame84(env, crop=False)
    if args.stack_frames > 1:
        env = FrameStack(env, args.stack_frames)
    env = ExtraTimeLimit(env, args.max_episode_steps)
    env = ImageToPyTorch(env)
    if args.normalize_env:
        env = NormalizedEnv(env)
    return env

def make_dm_lab(args):
    args = args.environment
    env = Dmlab_env(args)
    if args.clip_rewards:
        env = ClipRewardEnv(env)
    if args.skip_frames > 0:
        env = MaxAndSkipEnv(env, skip=args.skip_frames)
    if args.stack_frames > 1:
        env = FrameStack(env, args.stack_frames)
    env = ExtraTimeLimit(env, args.max_episode_steps)
    env = ImageToPyTorch(env)
    if args.normalize_env:
        env = NormalizedEnv(env)
    return env

def make_env(args):
    if args.environment.env_name == "SpaceInvaders-v0":
        return make_atari(args)
    elif args.environment.env_name == "seekavoid_arena_01":
        return make_dm_lab(args)
    else:
        raise NotImplemented
 